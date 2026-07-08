import cv2
import sys

cam = cv2.VideoCapture(0)
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #codec/ascii code to specify video capture (.mp4)
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cam.read()
    out.write(frame) #saves frame
    cv2.imshow('video', frame)
    
    if cv2.waitKey(1) & 0xff == ord('q'): break

cam.release()
out.release()
cv2.destroyAllWindows()