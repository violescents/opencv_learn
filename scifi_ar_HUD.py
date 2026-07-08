import cv2
import sys
import time
import numpy as np

def draw_hud_layer(width, height, timestamp):
    hud = np.zeros((height, width, 3), dtype=np.uint8)

    #colors (bgr)
    cyan = (255,242,0)
    red = (0,0,255)

    #center coords
    cx, cy = width //2, height //2

    #crosshair
    cv2.circle(hud, (cx, cy), 40, cyan, thickness = 1)
    cv2.circle(hud, (cx,cy), 2, red, thickness=-1) #centerdot
        #crosshair ticks
    cv2.line(hud, (cx - 60, cy), (cx-45,cy), cyan, 1)
    cv2.line(hud, (cx + 45, cy), (cx+60, cy), cyan, 1)
    cv2.line(hud, (cx,cy-60), (cx, cy-45), cyan, 1)
    cv2.line(hud, (cx, cy+45), (cx, cy + 60), cyan, 1)

    #corner tech brackets
    offset = 40
    bracket_len = 30
    #top left
    cv2.line(hud, (offset, offset), (offset + bracket_len, offset), cyan, 2)
    cv2.line(hud,(offset, offset), (offset, offset + bracket_len), cyan, 2)
    #bott rt
    cv2.line(hud, (width - offset, height - offset), (width - offset - bracket_len, height - offset), cyan, 2)
    cv2.line(hud, (width - offset, height - offset), (width - offset, height - offset - bracket_len), cyan, 2)

    #text overlays
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(hud, "Systemes: ONLINE", (50, 80), font, 0.6, cyan, 1, cv2.LINE_AA)
    cv2.putText(hud, f"TIME: {timestamp}", (50, 110), font, 0.5, cyan, 1, cv2.LINE_AA)

    #simulating dynamic pitch/yaw bar data
    cv2.putText(hud, "ALT: 245m", (width - 150, 80), font, 0.6, cyan, 1, cv2.LINE_AA)
    cv2.putText(hud, "SYS_LOCK: Acquired", (width - 200, height - 60), font, 0.5, red, 1, cv2.LINE_AA)

    return hud

def main():
    #init webcam
    cap = cv2.VideoCapture(0)

    print("HUD Started. press q to exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #mirror frame
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        
        #gen live timestamp
        current_time = time.strftime("%H:%M:%S", time.localtime())

        #draw hud elements onto an isolated black canvas layer
        hud_layer = draw_hud_layer(width, height, current_time)

        #alpha blend: merge webcame frame and HUD layer
        #weights: 1.0 (og vid opacity) + 0.8 (HUD graphics intensity)
        output_frame = cv2.addWeighted(frame, 1.0, hud_layer, 0.8, 0)

        #render final image window 
        cv2.imshow("Sci-Fi AR HUD", output_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()