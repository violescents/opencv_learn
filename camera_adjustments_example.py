#still need to work on this to see if it can apply to built in laptop webcam, but should in theory work for webcam

import cv2
import sys

def main():
    print(sys.argv[1])

    s_video = cv2.VideoCapture(int(sys.argv[1]), cv2.CAP_DSHOW)

    bright = 128
    focus = 0
    s_video.set(cv2.CAP_PROP_BRIGHTNESS, (bright))

    s_video.set(cv2.CAP_PROP_FOCUS, (focus))

    while True:
        ret, img = s_video.read()

        cv2.imshow("test screen", img)

        key = cv2.waitKey(1) & 0xff

        if key == ord('q'):
            s_video.release()
            break

        if key == ord(','):
            focus = focus -5
            if focus < 0:
                focus = 0
            s_video.set(cv2.CAP_PROP_FOCUS, (focus))

        if key == ord('='):
            bright = bright + 5
            s_video.set(cv2.CAP_PROP_FOCUS, (bright))

        if key == ord('-'):
            bright = bright - 5
            if bright < 0:
                bright = 0
            s_video.set(cv2.CAP_PROP_FOCUS, (bright))

        if key == ord('.'):
            focus = focus + 5 
            s_video.set(cv2.CAP_PROP_FOCUS, (focus))

if __name__ =='__main__':
    if len(sys.argv) !=2:
        print('Usage:')
        print('python camOptions.py <CAM Number')
        exit(-1)

    print('use +/- and </> keys (no shift) to adjust brightnes and focus, respectively')
    main()