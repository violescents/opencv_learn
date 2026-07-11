import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
from datetime import datetime
import numpy as np
import os
import sys

model_path = "pose_landmarker.task"
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.PoseLandmarkerOptions(base_options = base_options, running_mode= vision.RunningMode.VIDEO, output_segmentation_masks=False)
detector = vision.PoseLandmarker.create_from_options(options)
vid = cv2.VideoCapture(0)
fps = 30.0
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int (vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
raw_writer = cv2.VideoWriter("raw_webcam.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
draw_writer = cv2.VideoWriter("drawings.mp4", cv2.VideoWriter_fourcc(*"mp4v"),fps, (width, height))
trails = None

while vid.isOpened():
    ret,frame = vid.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    if trails is None:
        trails = np.zeros_like(frame)
    trails = cv2.addWeighted(trails, 0.85, np.zeros_like(trails), 0, 0)  # fade old lines

    raw_writer.write(frame)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = rgb_frame)
    timestamp_ms = int(vid.get(cv2.CAP_PROP_POS_MSEC))
    detection_result = detector.detect_for_video(mp_image, timestamp_ms)

    if detection_result.pose_landmarks:
        for pose_landmarks in detection_result.pose_landmarks:
            nose = pose_landmarks[0]
            left_elbow = pose_landmarks[13]
            left_wrist = pose_landmarks[15]
            right_elbow = pose_landmarks[14]
            right_wrist = pose_landmarks[16]
            left_knee = pose_landmarks[25]
            right_knee = pose_landmarks[26]
            right_ankle = pose_landmarks[28]
            left_ankle = pose_landmarks[27]
            left_shoulder = pose_landmarks[11]
            right_shoulder = pose_landmarks[12]

            h,w,_ = frame.shape
            #pixel positions:
            ple = (int(left_elbow.x * w), int(left_elbow.y*h))
            plw = (int(left_wrist.x*w), int(left_wrist.y*h))
            pre = (int(right_elbow.x*w), int(right_elbow.y*h))
            prw = (int(right_wrist.x *w), int(right_wrist.y*h))
            nx,ny = int(nose.x*w), int(nose.y*h)
            prk = (int(right_knee.x * w), int(right_knee.y*h))
            plk = (int(left_knee.x*w), int(left_knee.y*h))
            pra = (int(right_ankle.x*w), int(right_ankle.y*h))
            pla = (int(left_ankle.x*w), int(left_ankle.y*h))
            pls = (int(left_shoulder.x*w), int(left_shoulder.y*h))
            prs = (int(right_shoulder.x*w), int(right_shoulder.y*h))

            if left_elbow.presence > 0.7 and left_wrist.presence > 0.7:
                cv2.line(trails, ple, plw, (255, 0, 0), 3)
            if right_elbow.presence > 0.7 and right_wrist.presence > 0.7:
                cv2.line(trails, pre, prw, (255,0,0), 3)
            if nose.presence > 0.7:
                cv2.circle(trails, (nx, ny),5,(0,0,255), -1)
            if left_knee.presence > 0.7 and left_ankle.presence > 0.7:
                cv2.line(trails, plk, pla, (0,255,0), 3)
            if right_knee.presence > 0.7 and right_ankle.presence > 0.7:
                cv2.line(trails, prk, pra, (0,255,0), 3)
            if right_shoulder.presence>0.7 and right_elbow.presence > 0.7:
                cv2.line(trails, prs, pre, (255,255,255), 3)
            if left_shoulder.presence >0.7 and left_elbow.presence>0.7:
                cv2.line(trails, pls, ple, (255,255,255), 3)
    
    draw_frame = cv2.addWeighted(frame, 1.0, trails, 0.6, 0.0)
    cv2.imshow("webcam pose", draw_frame)

    raw_writer.write(frame)
    draw_writer.write(draw_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):break
raw_writer.release()
draw_writer.release()
vid.release()
cv2.destroyAllWindows()