#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import io
import cv2
import numpy as np
import math
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np

CAM_WIDTH = 80
CAM_HEIGHT = 60
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
    def __init__(self):
        self.pub = rospy.Publisher('gesture_cv', String, queue_size=10)

    def findDistance(self,A,B):
        return np.sqrt(np.power((A[0]-B[0]),2) + np.power((A[1]-B[1]),2))

    def run(self):
        while(1): #not rospy.is_shutdown():
     # Clear the IO of the previous buffer
            stream = io.BytesIO()
            lastOpen = 0
            lastClosed = 0
            prevcx1 = 0
            prevcy1 = 0
            swipeLeft = 0
            swipeRight = 0
            cancelCounter = 0
            msg = String()

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
                        if len(contours) > 1:
                            max_cnt2 = sortedContours[1]
			M1 = cv2.moments(max_cnt)
			cx1 = int(M1['m10']/M1['m00'])
			cy1 = int(M1['m01']/M1['m00'])+2
                        #cx1 = 0
                        #cy1 = 0
                        cx2 = 0
                        cy2 = 0
                        #peri = cv2.arcLength(max_cnt,True)
                        #approx = cv2.approxPolyDP(max_cnt, 0.005*peri, True)
                        #hull = cv2.convexHull(approx)

                        #minDist = np.inf
                        #minIndex = -1
                        #for i in range(len(hull)):
                        #    cv2.circle(frame,tuple(hull[i,0,:]),3,(0,255,255),-1)
                        #    dist = self.findDistance(hull[i,0,:], hull[(i+1)%len(hull),0,:])
                        #    if minDist > dist:
                        #        minDist = dist
                        #        minIndex = i
                        #    cx1 = hull[minIndex,0,0]
                        #    cy1 = hull[minIndex,0,1]
                        #offsetVec = hull[minIndex,0,:]-np.array([CAM_WIDTH/2, CAM_HEIGHT/2])




                        if len(contours)>1 and cv2.contourArea(max_cnt2) > 0.7*cv2.contourArea(max_cnt):
                            M2 = cv2.moments(max_cnt2)
                            cx2 = int(M2['m10']/M2['m00'])
                            cy2 = int(M2['m01']/M2['m00'])+2
                            #peri = cv2.arcLength(max_cnt2,True)
                            #approx = cv2.approxPolyDP(max_cnt2, 0.005*peri, True)
                            #hull = cv2.convexHull(approx)
                            #minDist = np.inf
                            #minIndex = -1
                            #for i in range(len(hull)):
                            #    cv2.circle(frame,tuple(hull[i,0,:]),3,(0,255,255),-1)
                            #    dist = self.findDistance(hull[i,0,:], hull[(i+1)%len(hull),0,:])
                            #    if minDist > dist:
                            #        minDist = dist
                            #        minIndex = i
                            #    cx2 = hull[minIndex,0,0]
                            #    cy2 = hull[minIndex,0,1]

                            dx = cx2 - cx1
                            dy = cy2 - cy1
                            #coords of mid point between hands
                            mpx = cx1+0.5*dx
                            mpy = cy1+0.5*dy

                            #cv2.drawContours(frame,[approx],0,(0,255,0),1)
                            zoomIn = 0
                            zoomOut = 0

                            handDist = np.sqrt(np.power(dx, 2)+ np.power (dy, 2))
                            if handDist < 26: #if hand closed
                                print "hand close detected"
                                lastClosed = time.time()
                                #print lastClosed
                                #print "lastcl - lastop =", lastClosed - lastOpen
                                if lastClosed - lastOpen < 3.5:
                                    msg = "ZoomIn"
                                    self.pub.publish(msg)
                                    print "zoomed in"
                                    lastOpen = 0

                            if handDist > 30: #if hand open
                                print "hand open detected"
                                lastOpen = time.time()
                                #print lastOpen
                                if lastOpen - lastClosed < 3.5:
                                    print "zoomed out"
                                    msg = "ZoomOut"
                                    self.pub.publish(msg)
                                    lastClosed = 0

                        elif -20 < cy1 - prevcy1 < 20:
                            if 10 < cx1 - prevcx1 < 40:
                                swipeLeft+=1
                                print 'swipeLeft', swipeLeft
                                if swipeLeft == 2:
                                    print 'SWIPE LEFT!'
                                    msg = "SwipeLeft"
                                    self.pub.publish(msg)
                                    swipeLeft = 0

                            elif 10 < prevcx1 - cx1 < 40:
                                swipeRight+=1
                                print 'swipeRight', swipeRight
                                if swipeRight == 2:
                                    print 'SWIPE RIGHT!'
                                    msg = "SwipeRight"
                                    self.pub.publish(msg)
                                    swipeRight = 0
                            else:
                                cancelCounter+=1
                                if cancelCounter == 3:
                                    swipeLeft = 0
                                    swipeRight = 0
                                    cancelCounter = 0
                        else:
                            cancelCounter+=1
                            if cancelCounter == 1:
                                swipeLeft = 0
                                swipeRight = 0
                                cancelCounter = 0


                        prevcx1 = cx1
                        prevcy1 = cy1

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
                #if len(contours) > 0 and calc:
                    #cv2.circle(skin, (cx1,cy1), 3, (0,0,255))
                    #cv2.circle(skin, (cx2,cy2), 3, (0,0,255))
		skin=cv2.flip(skin,1)
                # Display frame in a window
                #cv2.imshow('Frame',frame)
                cv2.imshow('Filtered Frame',skin)
                #cv2.imshow('mask',skinMask)
                interrupt=cv2.waitKey(1)
                # Quit by pressing 'q'
                if  interrupt & 0xFF == ord('q'):
                    break


if __name__ == '__main__':
    rospy.init_node('luko_cv', anonymous = True)
    vision = cv()
    vision.run()

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


