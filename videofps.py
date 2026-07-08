import cv2
import sys
import time

vid = cv2.VideoCapture(0)
frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

#init prev and new frame to calculate fps (time elapsed b/w frames)
prev_frame = 0
new_frame = 0

while True:
    ret, frame = vid.read()

    new_frame = time.time()

    
    time_diff = new_frame - prev_frame
    fps = 1 /time_diff if time_diff > 0 else 0 #avoids dividing by 0 on the first frame

    prev_frame = new_frame

    #conv fps to int then to str
    fps_text = f"FPS: {int(fps)}"

    #def text props
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (10,50)
    font_scale = 1
    color = (0, 255, 0)
    thickness = 2

    #draw fps counter onto frame
    cv2.putText(frame, fps_text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    out.write(frame)
    cv2.imshow('vid with fps', frame)

    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
    if key == ord('s'):
        cv2.imwrite('pic.png', frame)


vid.release()
out.release()
cv2.destroyAllWindows()