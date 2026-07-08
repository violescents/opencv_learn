import cv2
import sys
import time
from datetime import datetime
import numpy as np
import os

#config:
OUTPUT_DIR = "recordings"
BASE_NAME = "capture"

def generate_output_filename():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index = 1
    while True:
        filename = os.path.join(OUTPUT_DIR, f"{BASE_NAME}_{index:03d}.mp4")

        if not os.path.exists(filename):
            return filename
        
        index +=1

def open_camera():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise RuntimeError("womp womp, camera unable to open")
    return cam

def vid_writer(cam, filename):
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 0
    
    
    writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'),fps, (width, height))
    return writer
def fps_calc(prev_time):
    #fps calc:
    new = time.time()
    time_diff = new - prev_time
    fps = 1/time_diff if time_diff >0 else 0 #avoids dividing by 0
    return fps, new


def draw_hud(frame, frame_number, fps):
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
    overlay = frame.copy()
    cv2.rectangle(overlay, (10,10), (398,120), (30, 30, 30),-1)
    frame = cv2.addWeighted(overlay, 0.5, frame, 0.5,0)
    cv2.putText(frame, f"Timestamp:", (20,35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0),2)
    cv2.putText(frame, f"FPS: {fps:.2f}", (20,65), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
    cv2.putText(frame, f"Frame: {frame_number}", (20,95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

    return frame

def process(frame, frame_number, fps):
    frame = draw_hud(frame, frame_number, fps)
    return frame

def main():
    camera = open_camera()
    filename = generate_output_filename()
    writer = vid_writer(camera, filename)

    prev_time = time.time()

    frame_number = 0
    while True:
        ret, frame = camera.read()
        if not ret: break
        frame_number +=1
        fps, prev_time = fps_calc(prev_time)
        frame = process(frame, frame_number, fps)
        writer.write(frame)
        cv2.imshow("camera", frame)
        if cv2.waitKey(1) &0xff == ord('q'): break
    writer.release()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()