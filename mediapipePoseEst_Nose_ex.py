import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = "pose_landmarker.task"

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.PoseLandmarkerOptions(base_options = base_options, running_mode=vision.RunningMode.VIDEO, output_segmentation_masks=False)

#init detector
detector = vision.PoseLandmarker.create_from_options(options)

#init webcam
cap=cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data = rgb_frame)
    timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

    detection_result = detector.detect_for_video(mp_image, timestamp_ms)

    if detection_result.pose_landmarks:
        for pose_landmarks in detection_result.pose_landmarks:
            nose = pose_landmarks[0]
            h,w,c = frame.shape
            cx, cy = int(nose.x*w), int(nose.y*h)
            
            if nose.presence > 0.5: 
                cv2.circle(frame, (cx, cy),5,(0,255,0),-1)

    cv2.imshow('MediaPipe Tasks Pose Trakicking', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()