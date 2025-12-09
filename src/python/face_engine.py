# # face_engine.py
# """
# Face / frame analysis utilities.

# Provides:
# - analyze_frame(pil_image_or_cv2_img) -> dict with:
#     {
#       "eye_contact": int 0-100,
#       "visual_confidence": int 0-100,
#       "emotion": str,
#       "emotion_confidence": int 0-100,
#       "blink_ratio": float,
#       "head_pose": {"yaw": float, "pitch": float, "roll": float},
#       "raw_emotions": dict
#     }

# Notes:
# - Requires mediapipe, fer, mtcnn, opencv-python, numpy, pillow
# - Designed to be robust: returns reasonable defaults on error
# """

# from typing import Dict, Any, Tuple
# import numpy as np
# import cv2
# from PIL import Image
# import math
# import traceback

# # mediapipe & FER imports
# try:
#     import mediapipe as mp
# except Exception as e:
#     mp = None

# try:
#     from fer import FER
# except Exception:
#     FER = None

# # Initialize detectors lazily to avoid heavy import cost at module load
# _face_mesh = None
# _fer_detector = None

# def _init_face_mesh():
#     global _face_mesh
#     if _face_mesh is None and mp is not None:
#         _face_mesh = mp.solutions.face_mesh.FaceMesh(
#             static_image_mode=False,
#             max_num_faces=1,
#             refine_landmarks=True,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5,
#         )
#     return _face_mesh

# def _init_fer():
#     global _fer_detector
#     if _fer_detector is None and FER is not None:
#         try:
#             _fer_detector = FER(mtcnn=True)
#         except Exception:
#             # FER may fail to initialize with mtcnn on some platforms; fallback to no mtcnn
#             try:
#                 _fer_detector = FER(mtcnn=False)
#             except Exception:
#                 _fer_detector = None
#     return _fer_detector

# # -------------------------
# # Helpers: image conversions
# # -------------------------
# def pil_to_cv(img: Image.Image):
#     """PIL (RGB) -> OpenCV BGR"""
#     return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# def cv_to_rgb(img_cv):
#     return cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

# # -------------------------
# # Landmark utilities
# # -------------------------
# def landmarks_mean_xy(landmarks):
#     xs = [p.x for p in landmarks]
#     ys = [p.y for p in landmarks]
#     return float(np.mean(xs)), float(np.mean(ys))

# def get_eye_aspect_ratio(landmarks, left_indices, right_indices, img_w, img_h) -> Tuple[float, float]:
#     """
#     Compute average Eye Aspect Ratio (EAR) for left and right eye.
#     Uses normalized landmark coordinates -> convert to pixel coords.
#     Indices should reference mediapipe face mesh points.
#     """
#     def ear_for(indices):
#         pts = [(int(landmarks[i].x * img_w), int(landmarks[i].y * img_h)) for i in indices]
#         # simple approximation using vertical/horizontal distances
#         # ensure enough points
#         if len(pts) < 6:
#             return 0.0
#         # choose 2 vertical pairs and 1 horizontal
#         A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
#         B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
#         C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
#         if C == 0:
#             return 0.0
#         ear = (A + B) / (2.0 * C)
#         return float(ear)
#     left_ear = ear_for(left_indices)
#     right_ear = ear_for(right_indices)
#     return left_ear, right_ear

# # Typical mediapipe iris/eye landmark indices (approx). Using face_mesh refined landmarks:
# # we'll pick two small sets for EAR estimation (not exact — rough)
# LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]   # approximate
# RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380] # approximate

# # -------------------------
# # Head pose (very rough)
# # -------------------------
# def estimate_head_pose(landmarks, img_w, img_h):
#     """
#     Very rough head pose via 2D landmark positions: compute roll, yaw, pitch approximations.
#     This is approximate and not a professional headpose calculation.
#     """
#     # Use nose tip and eyes for a cheap estimation
#     try:
#         # choose nose tip and eye centers
#         nose = landmarks[1]   # not exact; fallback if index exists
#         left_eye = landmarks[33]
#         right_eye = landmarks[263]

#         nx, ny = nose.x, nose.y
#         lx, ly = left_eye.x, left_eye.y
#         rx, ry = right_eye.x, right_eye.y

#         dx = (rx - lx)
#         dy = (ry - ly)

#         # roll: angle of eye-line
#         roll = math.degrees(math.atan2(dy, dx))

#         # yaw: relative position of nose between eyes (- left, + right)
#         eye_center_x = (lx + rx) / 2.0
#         yaw = (nx - eye_center_x) * 200  # scaled

#         # pitch: relative vertical difference nose vs eyes
#         eye_center_y = (ly + ry) / 2.0
#         pitch = (ny - eye_center_y) * 200

#         return {"yaw": float(yaw), "pitch": float(pitch), "roll": float(roll)}
#     except Exception:
#         return {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}

# # -------------------------
# # Core analyze_frame
# # -------------------------
# def analyze_frame(pil_image) -> Dict[str, Any]:
#     """
#     Input: PIL.Image (RGB) OR OpenCV BGR numpy array.
#     Output: metrics dict.
#     """
#     # Defaults
#     default_metrics = {
#         "eye_contact": 50,
#         "visual_confidence": 50,
#         "emotion": "neutral",
#         "emotion_confidence": 50,
#         "blink_ratio": 0.0,
#         "head_pose": {"yaw": 0.0, "pitch": 0.0, "roll": 0.0},
#         "raw_emotions": {},
#     }

#     try:
#         # Convert to OpenCV BGR if PIL passed
#         if isinstance(pil_image, Image.Image):
#             img_cv = pil_to_cv(pil_image)
#         elif isinstance(pil_image, np.ndarray):
#             img_cv = pil_image.copy()
#         else:
#             return default_metrics

#         h, w = img_cv.shape[:2]
#         rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

#         # init detectors
#         face_mesh = _init_face_mesh()
#         fer_detector = _init_fer()

#         eye_contact_score = 0.0
#         blink_ratio = 0.0
#         head_pose = {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}

#         # Face mesh processing
#         if face_mesh is not None:
#             results = face_mesh.process(rgb)
#             if results and results.multi_face_landmarks:
#                 landmarks = results.multi_face_landmarks[0].landmark

#                 # center of face proximity to image center => eye contact heuristic
#                 cx, cy = landmarks_mean_xy(landmarks)
#                 dx = abs(cx - 0.5)
#                 dy = abs(cy - 0.5)
#                 dist = math.sqrt(dx*dx + dy*dy)
#                 # map distance to score (0..100)
#                 eye_contact_score = max(0.0, 1.0 - dist * 4.0) * 100.0
#                 eye_contact_score = max(0.0, min(100.0, eye_contact_score))

#                 # EAR-based blink detection
#                 left_ear, right_ear = get_eye_aspect_ratio(landmarks, LEFT_EYE_IDX, RIGHT_EYE_IDX, w, h)
#                 ear_avg = (left_ear + right_ear) / 2.0 if (left_ear + right_ear) > 0 else 0.0
#                 # typical EAR baseline ~0.25; lower -> blink
#                 blink_ratio = 0.0
#                 if ear_avg > 0:
#                     blink_ratio = float(1.0 / (ear_avg * 10.0))  # inverted scale (higher when eye closed)
#                     blink_ratio = max(0.0, min(5.0, blink_ratio))

#                 # head pose approximation
#                 head_pose = estimate_head_pose(landmarks, w, h)

#         # Emotion detection via FER
#         emotion = "neutral"
#         emotion_confidence = 50
#         raw_emotions = {}
#         if fer_detector is not None:
#             try:
#                 # FER expects BGR or RGB; it works with cv2 image directly
#                 fer_out = fer_detector.detect_emotions(img_cv)
#                 if fer_out and isinstance(fer_out, list) and len(fer_out) > 0:
#                     emotions_map = fer_out[0].get("emotions", {})
#                     raw_emotions = {k: float(v) for k, v in emotions_map.items()}
#                     if raw_emotions:
#                         top_em = max(raw_emotions, key=raw_emotions.get)
#                         emotion = top_em
#                         emotion_confidence = int(min(100, raw_emotions[top_em] * 100))
#             except Exception:
#                 # FER may raise if no face or other issues -- continue safely
#                 raw_emotions = {}

#         # Visual confidence: weighted combination of eye contact and positive emotions
#         positive_emotions = ["happy", "surprise"]
#         pos_score = sum(raw_emotions.get(e, 0.0) for e in positive_emotions)
#         visual_confidence = 0.6 * (eye_contact_score / 100.0) + 0.4 * pos_score
#         visual_confidence = float(max(0.0, min(1.0, visual_confidence)) * 100.0)

#         metrics = {
#             "eye_contact": int(round(eye_contact_score)),
#             "visual_confidence": int(round(visual_confidence)),
#             "emotion": emotion,
#             "emotion_confidence": int(round(emotion_confidence)),
#             "blink_ratio": round(float(blink_ratio), 3),
#             "head_pose": {
#                 "yaw": float(round(head_pose.get("yaw", 0.0), 2)),
#                 "pitch": float(round(head_pose.get("pitch", 0.0), 2)),
#                 "roll": float(round(head_pose.get("roll", 0.0), 2)),
#             },
#             "raw_emotions": raw_emotions,
#         }

#         return metrics

#     except Exception as e:
#         # On any failure, print traceback and return defaults
#         traceback.print_exc()
#         return default_metrics

# # Simple test helper (when running module directly)
# if __name__ == "__main__":
#     # quick smoke test (requires test.jpg in same dir)
#     import os
#     if os.path.exists("test.jpg"):
#         pil = Image.open("test.jpg").convert("RGB")
#         m = analyze_frame(pil)
#         print("Frame metrics:", m)
#     else:
#         print("Place a 'test.jpg' in this folder to run a smoke test.")









# src/python/face_engine.py
"""
Face / frame analysis utilities.
Optimized for Real-Time Video Feeds (Speed > Perfect Accuracy).
"""

from typing import Dict, Any, Tuple
import numpy as np
import cv2
from PIL import Image
import math
import traceback

# 1. Robust Imports
try:
    import mediapipe as mp
    MP_AVAILABLE = True
except ImportError:
    mp = None
    MP_AVAILABLE = False
    print("⚠️ Mediapipe not found. Visual analysis will be disabled.")

try:
    from fer import FER
    FER_AVAILABLE = True
except ImportError:
    FER = None
    FER_AVAILABLE = False
    print("⚠️ FER not found. Emotion analysis will be disabled.")

# 2. Lazy Global Initializers (Singleton Pattern)
_face_mesh = None
_fer_detector = None

def _init_face_mesh():
    global _face_mesh
    if _face_mesh is None and MP_AVAILABLE:
        _face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,       # Optimized for video streams
            max_num_faces=1,               # We only care about the candidate
            refine_landmarks=True,         # Better eye/iris tracking
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
    return _face_mesh

def _init_fer():
    global _fer_detector
    if _fer_detector is None and FER_AVAILABLE:
        try:
            # 🚀 SPEED OPTIMIZATION: mtcnn=False uses OpenCV (Faster)
            # mtcnn=True is too slow for real-time video feeds
            _fer_detector = FER(mtcnn=False) 
        except Exception as e:
            print(f"⚠️ FER Init Warning: {e}")
            _fer_detector = None
    return _fer_detector

# -------------------------
# Helpers
# -------------------------
def pil_to_cv(img: Image.Image):
    """PIL (RGB) -> OpenCV BGR"""
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# -------------------------
# Geometry Logic
# -------------------------
def landmarks_mean_xy(landmarks):
    xs = [p.x for p in landmarks]
    ys = [p.y for p in landmarks]
    return float(np.mean(xs)), float(np.mean(ys))

def get_eye_aspect_ratio(landmarks, left_indices, right_indices, img_w, img_h) -> Tuple[float, float]:
    """Calculates Eye Aspect Ratio (EAR) to detect blinking/drowsiness."""
    def ear_for(indices):
        pts = [(int(landmarks[i].x * img_w), int(landmarks[i].y * img_h)) for i in indices]
        if len(pts) < 6: return 0.0
        
        # Vertical distances
        A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
        B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
        # Horizontal distance
        C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
        
        if C == 0: return 0.0
        return (A + B) / (2.0 * C)

    left_ear = ear_for(left_indices)
    right_ear = ear_for(right_indices)
    return left_ear, right_ear

# Standard Mediapipe Eye Indices
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

def estimate_head_pose(landmarks, img_w, img_h):
    """
    Estimates Head Pose (Yaw, Pitch, Roll) using 2D landmarks.
    """
    try:
        nose = landmarks[1]
        left_eye = landmarks[33]
        right_eye = landmarks[263]

        nx, ny = nose.x, nose.y
        lx, ly = left_eye.x, left_eye.y
        rx, ry = right_eye.x, right_eye.y

        # Roll: Tilt of the head (angle between eyes)
        dx = (rx - lx)
        dy = (ry - ly)
        roll = math.degrees(math.atan2(dy, dx))

        # Yaw: Turning left/right (nose position relative to eyes)
        eye_center_x = (lx + rx) / 2.0
        yaw = (nx - eye_center_x) * 200  # Scaling factor for estimation

        # Pitch: Looking up/down
        eye_center_y = (ly + ry) / 2.0
        pitch = (ny - eye_center_y) * 200

        return {"yaw": float(yaw), "pitch": float(pitch), "roll": float(roll)}
    except Exception:
        return {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}

# -------------------------
# CORE FUNCTION: Analyze Frame
# -------------------------
def analyze_frame(pil_image) -> Dict[str, Any]:
    """
    Main entry point. Analyzes a single video frame.
    Returns: Emotion, Eye Contact Score, Confidence Score.
    """
    default_metrics = {
        "eye_contact": 0,
        "visual_confidence": 0,
        "emotion": "Neutral",
        "emotion_confidence": 0,
        "blink_ratio": 0.0,
        "head_pose": {"yaw": 0, "pitch": 0, "roll": 0},
        "raw_emotions": {}
    }

    # 1. Image Prep
    try:
        if isinstance(pil_image, Image.Image):
            img_cv = pil_to_cv(pil_image)
        elif isinstance(pil_image, np.ndarray):
            img_cv = pil_image.copy()
        else:
            return default_metrics

        h, w = img_cv.shape[:2]
        rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"❌ Image Error: {e}")
        return default_metrics

    # 2. Load Models
    face_mesh = _init_face_mesh()
    fer_detector = _init_fer()

    # 3. Analyze Geometry (Mediapipe)
    eye_contact_score = 50.0
    blink_ratio = 0.0
    head_pose = default_metrics["head_pose"]

    if face_mesh:
        results = face_mesh.process(rgb)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            # Eye Contact: Distance of nose from center of screen
            cx, cy = landmarks_mean_xy(landmarks)
            dist_from_center = math.sqrt((cx - 0.5)**2 + (cy - 0.5)**2)
            # Map 0.0 (center) -> 100, 0.3 (far) -> 0
            eye_contact_score = max(0.0, 1.0 - (dist_from_center * 3.5)) * 100

            # Blink Detection
            l_ear, r_ear = get_eye_aspect_ratio(landmarks, LEFT_EYE_IDX, RIGHT_EYE_IDX, w, h)
            avg_ear = (l_ear + r_ear) / 2.0
            if avg_ear > 0:
                blink_ratio = 1.0 / (avg_ear * 10.0)

            # Head Pose
            head_pose = estimate_head_pose(landmarks, w, h)

    # 4. Analyze Emotion (FER)
    emotion = "Neutral"
    emotion_conf = 0
    raw_emotions = {}

    if fer_detector:
        try:
            # FER returns list of faces: [{'box':..., 'emotions': {...}}]
            analysis = fer_detector.detect_emotions(img_cv)
            if analysis and len(analysis) > 0:
                top_face = analysis[0]
                emotions = top_face["emotions"]
                
                # Find dominant emotion
                emotion, val = max(emotions.items(), key=lambda item: item[1])
                emotion_conf = int(val * 100)
                raw_emotions = emotions
        except Exception:
            pass # FER failed gracefully

    # 5. Composite Score Calculation
    # Visual Confidence = Eye Contact + Positive Emotion + Stable Head
    positive_vibes = raw_emotions.get("happy", 0) + raw_emotions.get("neutral", 0)
    visual_confidence = (eye_contact_score * 0.5) + (positive_vibes * 100 * 0.3) + (50 * 0.2) # Base 20%

    return {
        "eye_contact": int(eye_contact_score),
        "visual_confidence": int(min(100, visual_confidence)),
        "emotion": emotion.capitalize(),
        "emotion_confidence": emotion_conf,
        "blink_ratio": round(blink_ratio, 2),
        "head_pose": {k: round(v, 1) for k, v in head_pose.items()},
        "raw_emotions": raw_emotions
    }

# -------------------------
# TEST HARNESS
# -------------------------
if __name__ == "__main__":
    if not MP_AVAILABLE or not FER_AVAILABLE:
        print("❌ Missing dependencies. Run: pip install mediapipe fer opencv-python")
    else:
        print("✅ Face Engine Loaded. Ready for frames.")