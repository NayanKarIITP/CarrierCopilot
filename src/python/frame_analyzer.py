# import cv2
# import base64
# import numpy as np
# import mediapipe as mp

# mp_face_mesh = mp.solutions.face_mesh

# # Landmarks for head pose & emotion heuristics
# NOSE_TIP = 1
# LEFT_EYE = 33
# RIGHT_EYE = 263
# CHIN = 152
# LEFT_MOUTH = 78
# RIGHT_MOUTH = 308


# def decode_base64_image(base64_str: str):
#     if "," in base64_str:
#         base64_str = base64_str.split(",")[1]
#     img_bytes = base64.b64decode(base64_str)
#     np_arr = np.frombuffer(img_bytes, np.uint8)
#     return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


# # ---------------------------
# #  EMOTION (Lightweight Model)
# # ---------------------------

# def predict_emotion(landmarks, w, h):
#     """Basic rule-based emotion estimation to match output consistency."""
    
#     # Mouth openness (smile indicator)
#     mouth_left = np.array([landmarks[LEFT_MOUTH].x * w, landmarks[LEFT_MOUTH].y * h])
#     mouth_right = np.array([landmarks[RIGHT_MOUTH].x * w, landmarks[RIGHT_MOUTH].y * h])
#     mouth_distance = np.linalg.norm(mouth_left - mouth_right)

#     # Eye openness (surprise indicator)
#     eye_left = landmarks[LEFT_EYE]
#     eye_right = landmarks[RIGHT_EYE]
#     eye_w = abs((eye_left.y - eye_right.y)) * h

#     # Threshold rules
#     if mouth_distance > 55:
#         return "happy"
#     if eye_w > 12:
#         return "surprised"
#     return "neutral"


# # ---------------------------
# #  HEAD POSE
# # ---------------------------

# def determine_head_direction(yaw, pitch, roll):
#     if yaw < -15:
#         return "looking_right"
#     elif yaw > 15:
#         return "looking_left"

#     if pitch < -12:
#         return "looking_up"
#     elif pitch > 12:
#         return "looking_down"

#     if roll > 15:
#         return "tilt_right"
#     elif roll < -15:
#         return "tilt_left"

#     return "center"


# def get_head_pose(landmarks, frame_w, frame_h):
#     model_points = np.array([
#         (0.0, 0.0, 0.0),          # Nose tip
#         (-30.0, -30.0, -30.0),    # Left eye
#         (30.0, -30.0, -30.0),     # Right eye
#         (0.0, 40.0, -20.0),       # Chin
#         (-20.0, 20.0, -20.0),     # Left mouth
#         (20.0, 20.0, -20.0),      # Right mouth
#     ])

#     image_points = np.array([
#         (landmarks[NOSE_TIP].x * frame_w, landmarks[NOSE_TIP].y * frame_h),
#         (landmarks[LEFT_EYE].x * frame_w, landmarks[LEFT_EYE].y * frame_h),
#         (landmarks[RIGHT_EYE].x * frame_w, landmarks[RIGHT_EYE].y * frame_h),
#         (landmarks[CHIN].x * frame_w, landmarks[CHIN].y * frame_h),
#         (landmarks[LEFT_MOUTH].x * frame_w, landmarks[LEFT_MOUTH].y * frame_h),
#         (landmarks[RIGHT_MOUTH].x * frame_w, landmarks[RIGHT_MOUTH].y * frame_h),
#     ], dtype="double")

#     focal_length = frame_w
#     cam_matrix = np.array([
#         [focal_length, 0, frame_w / 2],
#         [0, focal_length, frame_h / 2],
#         [0, 0, 1]
#     ])

#     dist_coeff = np.zeros((4, 1))

#     success, rotation_vector, translation_vector = cv2.solvePnP(
#         model_points,
#         image_points,
#         cam_matrix,
#         dist_coeff,
#         flags=cv2.SOLVEPNP_ITERATIVE,
#     )

#     rot_mat, _ = cv2.Rodrigues(rotation_vector)
#     _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(rot_mat)

#     pitch = float(euler_angles[0])
#     yaw = float(euler_angles[1])
#     roll = float(euler_angles[2])

#     direction = determine_head_direction(yaw, pitch, roll)
#     return direction, (yaw, pitch, roll)


# # ---------------------------
# #  MAIN FRAME ANALYZER
# # ---------------------------

# def analyze_frame(image_base64: str):
#     frame = decode_base64_image(image_base64)

#     if frame is None:
#         return {"success": False, "error": "Invalid image"}

#     h, w, _ = frame.shape

#     with mp_face_mesh.FaceMesh(
#         static_image_mode=False,
#         max_num_faces=1,
#         refine_landmarks=True,
#         min_detection_confidence=0.5,
#         min_tracking_confidence=0.5,
#     ) as fm:

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = fm.process(rgb)

#         if not results.multi_face_landmarks:
#             return {
#                 "success": True,
#                 "metrics": {
#                     "emotion": "no_face",
#                     "eye_contact": 0,
#                     "head_pose": "unknown",
#                     "angles": None,
#                     "confidence_score": 0.25
#                 }
#             }

#         landmarks = results.multi_face_landmarks[0].landmark

#         # Emotion (light model)
#         emotion = predict_emotion(landmarks, w, h)

#         # Head pose
#         head_pose, angles = get_head_pose(landmarks, w, h)

#         # Eye contact approx
#         eye_contact = 0.85 if head_pose == "center" else 0.4

#         return {
#             "success": True,
#             "metrics": {
#                 "emotion": emotion,
#                 "eye_contact": eye_contact,
#                 "head_pose": head_pose,
#                 "angles": {
#                     "yaw": angles[0],
#                     "pitch": angles[1],
#                     "roll": angles[2],
#                 },
#                 "confidence_score": 0.92
#             }
#         }







#frame_analyzer.py
import cv2
import base64
import numpy as np
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh

# Landmarks for head pose (Canonical Face Mesh Indices)
NOSE_TIP = 1
LEFT_EYE = 33
RIGHT_EYE = 263
CHIN = 152
LEFT_MOUTH = 61  # Changed to 61 (corner)
RIGHT_MOUTH = 291 # Changed to 291 (corner)

def decode_base64_image(base64_str: str):
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
        img_bytes = base64.b64decode(base64_str)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Image decode error: {e}")
        return None

# ---------------------------
#  EMOTION (Lightweight Heuristics)
# ---------------------------

def predict_emotion(landmarks, w, h):
    """
    Basic rule-based emotion estimation.
    For production, consider a ML model (like FER) if speed allows.
    """
    # Landmarks indices
    # Mouth: 61 (left), 291 (right), 0 (upper), 17 (lower)
    mouth_left = np.array([landmarks[61].x * w, landmarks[61].y * h])
    mouth_right = np.array([landmarks[291].x * w, landmarks[291].y * h])
    mouth_top = np.array([landmarks[0].x * w, landmarks[0].y * h])
    mouth_bottom = np.array([landmarks[17].x * w, landmarks[17].y * h])

    mouth_width = np.linalg.norm(mouth_left - mouth_right)
    mouth_height = np.linalg.norm(mouth_top - mouth_bottom)
    
    # Eye openness
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    eye_openness = abs(left_eye_top.y - left_eye_bottom.y) * h

    # Ratios (approximate)
    ratio = mouth_height / mouth_width if mouth_width > 0 else 0

    if ratio > 0.5: # Mouth open wide
        return "surprised"
    if ratio > 0.3 and mouth_width > (w * 0.15): # Wide smile
        return "happy"
    
    return "neutral"

# ---------------------------
#  HEAD POSE (PnP Solver)
# ---------------------------

def determine_head_direction(yaw, pitch, roll):
    if yaw < -15: return "looking_right" # Image perspective
    elif yaw > 15: return "looking_left"

    if pitch < -10: return "looking_down" # Pitch axis direction varies by model
    elif pitch > 10: return "looking_up"

    if roll > 15: return "tilt_right"
    elif roll < -15: return "tilt_left"

    return "center"

def get_head_pose(landmarks, frame_w, frame_h):
    # 3D Model Points (Generic Face)
    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corner
        (0.0, -330.0, -65.0),        # Chin
        (-150.0, -150.0, -125.0),    # Left Mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
    ], dtype="double")

    # Image Points from Landmarks
    image_points = np.array([
        (landmarks[NOSE_TIP].x * frame_w, landmarks[NOSE_TIP].y * frame_h),
        (landmarks[LEFT_EYE].x * frame_w, landmarks[LEFT_EYE].y * frame_h),
        (landmarks[RIGHT_EYE].x * frame_w, landmarks[RIGHT_EYE].y * frame_h),
        (landmarks[CHIN].x * frame_w, landmarks[CHIN].y * frame_h),
        (landmarks[LEFT_MOUTH].x * frame_w, landmarks[LEFT_MOUTH].y * frame_h),
        (landmarks[RIGHT_MOUTH].x * frame_w, landmarks[RIGHT_MOUTH].y * frame_h)
    ], dtype="double")

    # Camera Internals (Approximate)
    focal_length = frame_w
    center = (frame_w / 2, frame_h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1)) # Assuming no lens distortion

    # Solve PnP
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return "unknown", (0, 0, 0)

    # Convert Rotation Vector to Matrix
    rmat, _ = cv2.Rodrigues(rotation_vector)

    # Calculate Euler Angles (Manual Calculation for Robustness)
    # Pitch (x), Yaw (y), Roll (z)
    sy = math.sqrt(rmat[0, 0] * rmat[0, 0] + rmat[1, 0] * rmat[1, 0])
    singular = sy < 1e-6

    if not singular:
        x = math.atan2(rmat[2, 1], rmat[2, 2])
        y = math.atan2(-rmat[2, 0], sy)
        z = math.atan2(rmat[1, 0], rmat[0, 0])
    else:
        x = math.atan2(-rmat[1, 2], rmat[1, 1])
        y = math.atan2(-rmat[2, 0], sy)
        z = 0

    pitch = math.degrees(x)
    yaw = math.degrees(y)
    roll = math.degrees(z)

    direction = determine_head_direction(yaw, pitch, roll)
    return direction, (yaw, pitch, roll)

# ---------------------------
#  MAIN FRAME ANALYZER
# ---------------------------

def analyze_frame(image_base64: str):
    frame = decode_base64_image(image_base64)

    if frame is None:
        return {"success": False, "error": "Invalid image"}

    h, w, _ = frame.shape

    # Use context manager for FaceMesh
    with mp_face_mesh.FaceMesh(
        static_image_mode=True, # True is better for single frame analysis
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

        # 1. Analyze Emotion
        emotion = predict_emotion(landmarks, w, h)

        # 2. Analyze Head Pose
        head_pose, angles = get_head_pose(landmarks, w, h)

        # 3. Calculate Visual Confidence Score
        # Start with base 50. 
        # +20 for center gaze. 
        # +20 for happy/neutral (calm).
        # -20 for extreme looking away.
        conf_score = 50
        if head_pose == "center":
            conf_score += 30
        elif "looking" in head_pose:
            conf_score -= 20
        
        if emotion in ["happy", "neutral"]:
            conf_score += 20
        
        conf_score = max(0, min(100, conf_score))

        # Eye Contact (Binary-ish)
        eye_contact = 100 if head_pose == "center" else 20

        return {
            "success": True,
            "metrics": {
                "emotion": emotion.capitalize(),
                "eye_contact": eye_contact,
                "head_pose": head_pose.replace("_", " ").title(),
                "angles": {
                    "yaw": round(angles[0], 1),
                    "pitch": round(angles[1], 1),
                    "roll": round(angles[2], 1),
                },
                "confidence_score": conf_score
            }
        }