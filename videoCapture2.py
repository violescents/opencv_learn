#different wayy to capture video
import cv2
import sys

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret,img = cam.read()
    cv2.imshow("vid", img)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        cam.release()
        break
    if key == ord('s'): #capture screenshot/img and save it to local file 
        cv2.imwrite('test.png', img)