import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#init mediapipe pose and drawing comps
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_rawing_styles = mp.solutions.drawing_styles

vid = cv2.VideoCapture(0)

with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation = False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while vid.isOpened():
        ret, frame = vid.read()
        if not ret: 
            print("ignore empty cam frame") 
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            h, w, c = frame.shape
            cx, cy = int(left_wrist.x * w), int(left_wrist.y*h)

            if left_wrist.visibility > 0.5:
                print(f"Left Wrist -X: {cx}, Y: {cy}")
        cv2.imshow('MediaPipe Pose Tracking', frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()