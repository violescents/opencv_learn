import cv2
import math
import numpy as np

clicked_points = []

def click_event(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(clicked_points)<3: clicked_points.append((x,y))

def calc_angle(p1, p2, p3):
    #cr8 vectors rel to vertex (p2)
    v1 = np.array([p1[0] - p2[0], p1[1]-p2[1]], dtype = float)
    v2 = np.array([p3[0]-p2[0], p3[1]-p2[1]], dtype = float)

    dot_product = np.dot(v1,v2)
    mag1 = np.linalg.norm(v1)
    mag2 = np.linalg.norm(v2)
    if mag1 ==0 or mag2 == 0: return 0.0
    cos_angle = dot_product / (mag1*mag2)
    cos_angle = np.clip(cos_angle, -1.0, 1.0) #clip cosine angle to safe range to avoid math domain errors
    angle = math.degrees(math.acos(cos_angle))
    return angle

window_name = "live angle nd dist tracker"
cap = cv2.VideoCapture(0)
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, click_event)

print("Instructions:\n- Left click three times to measure, p2 is the vertex\n- press 's' to save image\n- press 'c' to clear points\n- press 'q' to quit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: 
        print("womp womp")
        break

    display_frame = frame.copy()

    for idx, point in enumerate(clicked_points):
        cv2.circle(display_frame, point, 5, (0,0,255), -1)
        labels = ["1st pt", "2nd pt", "3rd pt"]
        cv2.putText(display_frame, labels[idx], (point[0] + 12, point[1] - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)


    if len(clicked_points) >= 2:
        p1, p2 = clicked_points[0], clicked_points[1]
        cv2.line(display_frame, p1, p2, (0,255,0),2)
        dist1 = math.hypot(p2[0] - p1[0],p2[1]-p1[1])
        mid1 = (int((p1[0]+p2[0])/2), int((p1[1] + p2[1])/2))
        cv2.putText(display_frame, f"{dist1:.1f}px", mid1, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0),1)
    if len(clicked_points) == 3:
        p2, p3 = clicked_points[1], clicked_points[2]
        cv2.line(display_frame, p2, p3, (0,255,0),2)
        dist2= math.hypot(p3[0]-p2[0],p3[1]-p2[1])
        mid2 = (int((p2[0]+p3[0])/2), int((p2[1]+p3[1])/2))
        cv2.putText(display_frame, f"{dist2:.1f}px",mid2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0),1)
        angle = calc_angle(p1,p2,p3)
        cv2.putText(display_frame, f"angle: {angle:.1f} deg", (p2[0]+15, p2[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255),2)

    cv2.imshow(window_name,display_frame)


    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        filename = "measured_angle.png"
        cv2.imwrite(filename, display_frame)
        print(f"saved snapshot successfully to {filename}!")
    elif key == ord('c'):
        clicked_points = []
        print("reset")
    elif key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()