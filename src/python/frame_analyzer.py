
# src/python/frame_analyzer.py
import cv2
import base64
import numpy as np
import math
import logging

# Setup Logger
logger = logging.getLogger(__name__)

# SAFE MEDIAPIPE IMPORT
HAS_MEDIAPIPE = False
mp = None
mp_face_mesh = None

try:
    import mediapipe as _mp
    mp = _mp
    mp_face_mesh = mp.solutions.face_mesh
    HAS_MEDIAPIPE = True
    logger.info(" MediaPipe loaded successfully")
except Exception as e:
    logger.warning(f" MediaPipe unavailable. Running in safe mode: {e}")
    HAS_MEDIAPIPE = False


# LANDMARK CONSTANTS
NOSE_TIP = 1
LEFT_EYE = 33
RIGHT_EYE = 263
CHIN = 152
LEFT_MOUTH = 61
RIGHT_MOUTH = 291


# UTILITIES

def decode_base64_image(base64_str: str):
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
        img_bytes = base64.b64decode(base64_str)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        logger.error(f"Image decode error: {e}")
        return None


# EMOTION LOGIC
def predict_emotion(landmarks, w, h):
    try:
        mouth_left = np.array([landmarks[61].x * w, landmarks[61].y * h])
        mouth_right = np.array([landmarks[291].x * w, landmarks[291].y * h])
        mouth_top = np.array([landmarks[0].x * w, landmarks[0].y * h])
        mouth_bottom = np.array([landmarks[17].x * w, landmarks[17].y * h])

        mouth_width = np.linalg.norm(mouth_left - mouth_right)
        mouth_height = np.linalg.norm(mouth_top - mouth_bottom)

        ratio = mouth_height / mouth_width if mouth_width > 0 else 0

        if ratio > 0.45:
            return "Surprised"
        if ratio > 0.25 and mouth_width > (w * 0.16):
            return "Happy"

        return "Focused"
    except Exception:
        return "Neutral"


# HEAD POSE (PnP)
def get_head_pose_pnp(landmarks, frame_w, frame_h):
    model_points = np.array([
        (0.0, 0.0, 0.0),
        (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0),
        (0.0, -330.0, -65.0),
        (-150.0, -150.0, -125.0),
        (150.0, -150.0, -125.0)
    ], dtype="double")

    image_points = np.array([
        (landmarks[NOSE_TIP].x * frame_w, landmarks[NOSE_TIP].y * frame_h),
        (landmarks[LEFT_EYE].x * frame_w, landmarks[LEFT_EYE].y * frame_h),
        (landmarks[RIGHT_EYE].x * frame_w, landmarks[RIGHT_EYE].y * frame_h),
        (landmarks[CHIN].x * frame_w, landmarks[CHIN].y * frame_h),
        (landmarks[LEFT_MOUTH].x * frame_w, landmarks[LEFT_MOUTH].y * frame_h),
        (landmarks[RIGHT_MOUTH].x * frame_w, landmarks[RIGHT_MOUTH].y * frame_h)
    ], dtype="double")

    focal_length = frame_w
    center = (frame_w / 2, frame_h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vector, _ = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs
    )

    if not success:
        return (0, 0, 0)

    rmat, _ = cv2.Rodrigues(rotation_vector)
    sy = math.sqrt(rmat[0, 0] ** 2 + rmat[1, 0] ** 2)

    if sy > 1e-6:
        x = math.atan2(rmat[2, 1], rmat[2, 2])
        y = math.atan2(-rmat[2, 0], sy)
        z = math.atan2(rmat[1, 0], rmat[0, 0])
    else:
        x = math.atan2(-rmat[1, 2], rmat[1, 1])
        y = math.atan2(-rmat[2, 0], sy)
        z = 0

    return (math.degrees(y), math.degrees(x), math.degrees(z))


# MAIN ANALYZER

def analyze_frame(image_base64: str):

    # SAFE MODE: MediaPipe unavailable
    if not HAS_MEDIAPIPE:
        return {
            "success": True,
            "metrics": {
                "emotion": "Unavailable",
                "eye_contact": 0,
                "head_pose": "Disabled",
                "angles": {"yaw": 0, "pitch": 0, "roll": 0},
                "confidence_score": 0
            }
        }

    frame = decode_base64_image(image_base64)
    if frame is None:
        return {"success": False, "error": "Invalid image"}

    h, w, _ = frame.shape

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as fm:

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = fm.process(rgb)

        if not results.multi_face_landmarks:
            return {
                "success": True,
                "metrics": {
                    "emotion": "No Face",
                    "eye_contact": 0,
                    "head_pose": "Unknown",
                    "angles": {"yaw": 0, "pitch": 0, "roll": 0},
                    "confidence_score": 0
                }
            }

        landmarks = results.multi_face_landmarks[0].landmark

        yaw, pitch, roll = get_head_pose_pnp(landmarks, w, h)

        for angle_name, angle in zip(
            ["yaw", "pitch", "roll"], [yaw, pitch, roll]
        ):
            if abs(angle) > 100:
                angle = 180 - angle if angle > 0 else -180 - angle

        head_pose_label = "Center"
        if abs(yaw) > 20:
            head_pose_label = "Turning"
        if abs(pitch) > 15:
            head_pose_label = "Tilting"

        emotion = predict_emotion(landmarks, w, h)

        conf_score = 75
        if head_pose_label == "Center":
            conf_score += 10
        elif abs(yaw) > 30 or abs(pitch) > 25:
            conf_score -= 40
        if emotion in ["Happy", "Focused", "Surprised"]:
            conf_score += 15

        conf_score = max(10, min(100, conf_score))

        deviation = math.sqrt(yaw ** 2 + pitch ** 2)
        eye_contact = max(0, 100 - (deviation * 2.5))

        return {
            "success": True,
            "metrics": {
                "emotion": emotion,
                "eye_contact": int(eye_contact),
                "head_pose": head_pose_label,
                "angles": {
                    "yaw": round(yaw, 1),
                    "pitch": round(pitch, 1),
                    "roll": round(roll, 1)
                },
                "confidence_score": int(conf_score)
            }
        }
