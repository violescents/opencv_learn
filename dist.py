import cv2
import math
import numpy as np

clicked_points = []

def click_event(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(clicked_points)>2: clicked_points.append((x,y))

window_name = "live dist tracker"
cap = cv2.VideoCapture(0)
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, click_event)

print("Instructions:\n- Left click twice to measure\n- press 's' to save image\n- press 'c' to clear points\n- press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret: 
        print("womp womp")
        break

    display_frame = frame.copy()

    for idx, point in enumerate(clicked_points):
        cv2.circle(display_frame, point, 5, (0,0,255), -1)
        label = "1st point" if idx == 0 else "2nd point"
        cv2.putText(display_frame, label, (point[0] + 110, point[1] - 10), cv2.FONT_HERSHE_SIMPLEX, 0.5, (0,0,255), 1)

        if len(clicked_points) == 2:
            pt1, pt2 = clicked_points[0], clicked_points[1]
            cv2.line(display_frame, pt1, pt2, (0, 255, 0), 2)
            distance = math.sqrt((pt2[0] - pt1[0])**2 + (pt2[1]-pt1[1])**2)
            mid_x = int((pt1[0] + pt2[0])/2)
            mid_y = int((pt1[1] + pt2[1]) / 2)
            distance_text = f"{distance:.2f} px"
            cv2.putText(display_frame, distance_text, (mid_x + 10, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

        cv2.imshow(window_name, display_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = "measured_distance.png"
            cv2.imwrite(filename, display_frame)
            print(f"saved snapshot successfully to {filename}!")
        elif key == ord('c'):
            clicked_points = []
            print("reset")
        elif key == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()