

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
    print(" Mediapipe not found. Visual analysis will be disabled.")

try:
    from fer import FER
    FER_AVAILABLE = True
except ImportError:
    FER = None
    FER_AVAILABLE = False
    print(" FER not found. Emotion analysis will be disabled.")

# 2. Lazy Global Initializers 
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
            _fer_detector = FER(mtcnn=False) 
        except Exception as e:
            print(f"⚠️ FER Init Warning: {e}")
            _fer_detector = None
    return _fer_detector

# Helpers
def pil_to_cv(img: Image.Image):
    """PIL (RGB) -> OpenCV BGR"""
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# Geometry Logic
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

# CORE FUNCTION: Analyze Frame

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
        print(f" Image Error: {e}")
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
    positive_vibes = raw_emotions.get("happy", 0) + raw_emotions.get("neutral", 0)
    visual_confidence = (eye_contact_score * 0.5) + (positive_vibes * 100 * 0.3) + (50 * 0.2) 

    return {
        "eye_contact": int(eye_contact_score),
        "visual_confidence": int(min(100, visual_confidence)),
        "emotion": emotion.capitalize(),
        "emotion_confidence": emotion_conf,
        "blink_ratio": round(blink_ratio, 2),
        "head_pose": {k: round(v, 1) for k, v in head_pose.items()},
        "raw_emotions": raw_emotions
    }


# TEST HARNESS

if __name__ == "__main__":
    if not MP_AVAILABLE or not FER_AVAILABLE:
        print(" Missing dependencies. Run: pip install mediapipe fer opencv-python")
    else:
        print(" Face Engine Loaded. Ready for frames.")