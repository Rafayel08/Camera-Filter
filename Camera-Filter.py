import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat

cap = cv2.VideoCapture(1) #Or whatever Video Capture device you want to use to get the normal Video(not virtual cam)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 10 #Or whatever you want to set the fps to

with pyvirtualcam.Camera(width, height, fps=fps, fmt=PixelFormat.BGR, device="OBS Virtual Camera") as cam:

    while True:
        #Input your filter between the while True and cam.send(frame):
        #In this example I put in a filter which traces an outline of anything that moves
        ret, Prev_frame= cap.read()
        ret, Current_frame=cap.read()
        if not ret:
            raise RuntimeError('Error fetching frame')
    
        frame_diff= cv2.absdiff(Current_frame, Prev_frame)
        imgray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(imgray, (5,5), 0)
        ret, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        frame=cv2.drawContours(frame_diff, contours, -1, (0, 255, 0), 3)

        cam.send(frame)

        cam.sleep_until_next_frame()
        Prev_frame=Current_frame