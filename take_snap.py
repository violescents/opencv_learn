import cv2
import sys

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

ret, img = cam.read()

cv2.imshow("video", img)

cv2.waitKey()

cam.release()