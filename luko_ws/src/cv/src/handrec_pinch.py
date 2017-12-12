#!/usr/bin/env python

import rospy
from cv.msg import Radial
import io
import cv2
import numpy as np
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np

CAM_WIDTH = 320
CAM_HEIGHT = 240
LUKO_HEIGHT = 35
LUKO_DISTANCE = 20
SCALING_FACTOR_PHI = 1.0
SCALING_FACTOR_D = 0.1 # pixel to distance ratio

# Initialise camera, allow it to warm up
camera = PiCamera(resolution = (CAM_WIDTH,CAM_HEIGHT))
rawCapture = PiRGBArray(camera)
time.sleep(0.1)

# HSV colour tolerances
lower = np.array([0,30,50], dtype=np.uint8)
upper = np.array([30,255,255], dtype=np.uint8)

class cv:
    #def __init__(self):
        #self.pub = rospy.Publisher('chatter', Radial, queue_size=10)

    def findDistance(self,A,B):
        return np.sqrt(np.power((A[0]-B[0]),2) + np.power((A[1]-B[1]),2))

    def run(self):
        while(1): #not rospy.is_shutdown():
     # Clear the IO of the previous buffer
            stream = io.BytesIO()
            lastOpen = 0
            lastClosed = 0
            for raw in camera.capture_continuous(stream,format='jpeg'):
                frame = cv2.imdecode(np.fromstring(stream.getvalue(),dtype=np.uint8),1)
                stream.truncate()
                stream.seek(0)
                #print "aaa"
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
                        sortedContours = sorted(contours,key = cv2.contourArea, reverse=True)
                        max_cnt  = sortedContours[0]
			max_cnt2 = sortedContours[1]
			M1 = cv2.moments(max_cnt)
			cx1 = int(M1['m10']/M1['m00'])
			cy1 = int(M1['m01']/M1['m00'])
                        cx2 = 0
                        cy2 = 0


                        if cv2.contourArea(max_cnt2) > 0.7*cv2.contourArea(max_cnt):
                            M2 = cv2.moments(max_cnt2)
                            cx2 = int(M2['m10']/M2['m00'])
                            cy2 = int(M2['m01']/M2['m00'])
                            dx = cx2 - cx1
                            dy = cy2 - cy1
                            #coords of mid point between hands
                            mpx = cx1+0.5*dx
                            mpy = cy1+0.5*dy

                            #cv2.drawContours(frame,[approx],0,(0,255,0),1)
                            zoomIn = 0
                            zoomOut = 0
                            
                            handDist = np.sqrt(np.power(dx, 2)+ np.power (dy, 2))
                            if handDist < 100: #if hand closed
                                print "hand close detected"
                                lastClosed = time.time()
                                #print lastClosed
                                #print "lastcl - lastop =", lastClosed - lastOpen
                                if lastClosed - lastOpen < 1:
                                    print "zoomed in"

                            if handDist > 150: #if hand open
                                print "hand open detected"
                                lastOpen = time.time()
                                #print lastOpen
                                if lastOpen - lastClosed < 1:
                                    print "zoomed out"

#                            curr = time.time()
#                            if curr - lastOpen > 0.7

                            '''
                            if handDist < 100: #if hand closed
                                handClosed = 1
                                prevTime = time.time()
                                if handOpen == 1: #if hand was open 500ms ago
                                    zoomOut = 1
                                    handOpen = 0
                                #time.sleep(0.25)
                                currentTime = time.time()

                            if handDist > 200: #if hand open
                                handOpen = 1
                                if handClosed == 1: #if hand was closed 500ms ago
                                    zoomIn = 1
                                    handClosed = 0
                              #time.sleep(0.25)

                            print handOpen
                            print handClosed
                            print zoomIn
                            Print zoomOut
                            zoomIn = 0
                            zoomOut = 0
                            handClosed = 0
                            handOpen = 0
'''
			#msg = Radial()
                        #msg.radius = new_luko_dist
                        #msg.theta = theta
                        #self.pub.publish(msg)

                        #cv2.circle(frame,tuple(hull[minIndex,0,:]),3,(163,50,204),-1)
                        cv2.circle(frame, (cx1,cy1), 3, (0,0,255), -1)
                        cv2.circle(frame, (cx2,cy2), 3, (0,0,255), -1)
                        #cv2.drawContours(frame,[approx],0,(0,255,0),1)
                        calc = True
                        #print calc
                    except Exception as e:
                        calc = False
                        print e

                #print "about to show frame"
		# Operations on the frame
                skin = cv2.bitwise_and(frame, frame, mask = skinMask)
                if len(contours) > 0 and calc:
                    cv2.circle(skin, (cx1,cy1), 3, (0,0,255))
                    #cv2.circle(skin, (cx2,cy2), 3, (0,0,255))
		skin=cv2.flip(skin,1)
                # Display frame in a window
                cv2.imshow('Frame',frame)
                cv2.imshow('Filtered Frame',skin)
                #cv2.imshow('mask',skinMask)
                interrupt=cv2.waitKey(1)
                # Quit by pressing 'q'
                if  interrupt & 0xFF == ord('q'):
                    break


if __name__ == '__main__':
    #rospy.init_node('luko_cv', anonymous = True)
    vision = cv()
    vision.run()

