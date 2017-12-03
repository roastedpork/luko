#!/usr/bin/python


import io
import cv2
import numpy as np
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

# Camera
camera = PiCamera(resolution = (320,240))
rawCapture = PiRGBArray(camera)
time.sleep(0.1)

# HSV colour tolerances
lower = np.array([0,30,50], dtype=np.uint8)
upper = np.array([30,255,255], dtype=np.uint8)


try:

    while(1):
        calc = False
        # Clear the IO of the previos buffer
        stream = io.BytesIO()
        for raw in camera.capture_continuous(stream,format='jpeg'):
            frame = cv2.imdecode(np.fromstring(stream.getvalue(),dtype=np.uint8),1)
            stream.truncate()
            stream.seek(0)

            # Convert to HSV colour space
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            skinMask = cv2.inRange(frame_hsv, lower, upper)

            # apply erosion, dilation and blurring to mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
            skinMask = cv2.erode(skinMask, kernel, iterations=1)
            skinMask = cv2.dilate(skinMask, kernel, iterations=1)
            skinMask = cv2.GaussianBlur(skinMask, (3,3), 0)
            
            # calculate centroid
            img, contours, _ = cv2.findContours(skinMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                try:
                    max_cnt = sorted(contours,key = cv2.contourArea, reverse=True)[0]
                    M = cv2.moments(max_cnt)
                    cx = int(M['m10']/M['m00'])  
                    cy = int(M['m01']/M['m00'])
                    
                    peri = cv2.arcLength(max_cnt,True)
                    approx = cv2.approxPolyDP(max_cnt, 0.0025*peri, True)
                    hull = cv2.convexHull(approx)
                    for i in range(len(hull)):
                        cv2.circle(frame,tuple(hull[i,0,:]),3,(0,255,255),-1)
                    cv2.circle(frame, (cx,cy), 3, (0,0,255), -1)
                    cv2.drawContours(frame,[approx],0,(0,255,0),1)
                    
                    
                    
                    calc = True
                except:
                    calc = False
            
            # Operations on the frame
            skin = cv2.bitwise_and(frame, frame, mask = skinMask)
            if len(contours) > 0 and calc:
                cv2.circle(skin, (cx,cy), 3, (0,0,255))
                #cv2.drawContours(skin,[hull],0,(0,255,0),2)

            skin=cv2.flip(skin,1)

            # Display frame in a window
            cv2.imshow('Frame',frame)
            cv2.imshow('Filtered Frame',skin)
            cv2.imshow('mask',skinMask)
            interrupt=cv2.waitKey(1)
    
            # Quit by pressing 'q'
            if  interrupt & 0xFF == ord('q'):
                break

except KeyboardInterrupt, TypeError:       
    # Release camera & end program
    camera.release()
    cv2.destroyAllWindows()
