import cv2

#open default cam
cam = cv2.VideoCapture(0)

#get default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#define codec and create videowriter object
fourcc =  cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cam.read()

    #write the frame to the output file
    out.write(frame)

    #display captured frame
    cv2.imshow('Camera', frame)

    #press q to exit loop
    if cv2.waitKey(1) == ord('q'):
        break

#release the capture
cam. release()
out.release()
cv2.destroyAllWindows()