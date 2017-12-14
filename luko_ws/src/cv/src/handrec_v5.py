#!/usr/bin/env python

import rospy
from mbed_interface.msg import JointAngles
from sensor_msgs.msg import JointState
from speech_recognition.msg import Intent
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
SCALING_FACTOR_PHI = 0.1
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
        self.pub = rospy.Publisher('mbed/set_target_angle', JointAngles, queue_size=10)
        self.sub = rospy.Subscriber('mbed/joint_states', JointState, self.callback, queue_size=10)
        self.subAct = rospy.Subscriber('intent/movement', Intent, self.callback_act, queue_size=10)
        self.current = [0 for i in range(5)]

        self.pub_intent = rospy.Subscriber('intent/movement', Intent, self.callback_action, queue_size=10)
        self.start = True

    def callback(self, data):
        self.current = np.array(data.position)

    def callback_act(self, data):
        action = data.action
        if action == "target":
            print
        else:
            pass

    def findDistance(self,A,B):
        return np.sqrt(np.power((A[0]-B[0]),2) + np.power((A[1]-B[1]),2))

    def callback_action(self, data):
        self.start = True

    def filterSkin(self,frame):
        # Convert to HSV colour space
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        skinMask = cv2.inRange(frame_hsv, lower, upper)

        # apply erosion, dilation and blurring to mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
        skinMask = cv2.erode(skinMask, kernel, iterations=1)
        skinMask = cv2.dilate(skinMask, kernel, iterations=1)
        skinMask = cv2.GaussianBlur(skinMask, (3,3), 0)
        return skinMask

    def getHull(self, cnts):
        max_cnt = sorted(cnts,key = cv2.contourArea, reverse=True)[0]
        M = cv2.moments(max_cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        peri = cv2.arcLength(max_cnt,True)
        approx = cv2.approxPolyDP(max_cnt, 0.005*peri, True)
        hull = cv2.convexHull(approx)

        return (cx,cy), approx, hull

    def run(self):
        while not rospy.is_shutdown():
        # Clear the IO of the previous buffer
            stream = io.BytesIO()
            for raw in camera.capture_continuous(stream,format='jpeg'):
                frame = cv2.imdecode(np.fromstring(stream.getvalue(),dtype=np.uint8),1)
                stream.truncate()
                stream.seek(0)
                if self.start:
                    skinMask = self.filterSkin(frame)
                    # calculate centroid
                    img, contours, _ = cv2.findContours(skinMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    if len(contours) > 0:
                        try:
                            (cx,cy), approx, hull = self.getHull(contours)
                            minDist = np.inf
                            minIndex = -1
                            for i in range(len(hull)):
                                cv2.circle(frame,tuple(hull[i,0,:]),3,(0,255,255),-1)
                                dist = self.findDistance(hull[i,0,:], hull[(i+1)%len(hull),0,:])
                                if minDist > dist:
                                    minDist = dist
                                    minIndex = i

                            offsetVec = hull[minIndex,0,:]-np.array([CAM_WIDTH/2, CAM_HEIGHT/2])
                            print offsetVec*SCALING_FACTOR_D
                            phi = np.arctan2(offsetVec[1],offsetVec[0])
                            print np.degrees(phi)

                            offsetDist = np.linalg.norm(offsetVec)*SCALING_FACTOR_D

                            # cosine rule
                            theta = np.pi/2 - phi
                            new_luko_dist = np.sqrt(offsetDist*offsetDist + LUKO_DISTANCE*LUKO_DISTANCE - 2*offsetDist*LUKO_DISTANCE*np.cos(theta))
                            print theta, new_luko_dist
                            delta_rot = np.arcsin(np.sin(theta)/new_luko_dist * offsetDist)
                            delta_y = new_luko_dist - LUKO_DISTANCE
                            print np.degrees(delta_rot),delta_y

                            msg = JointAngles()
                            delta = np.degrees(theta)*SCALING_FACTOR_PHI
                            msg.joints = self.current + np.array([delta, 0, 0, 0, 0])
                            if abs(delta) < 2:
                                self.start = False
                            self.pub.publish(msg)

                            cv2.circle(frame,tuple(hull[minIndex,0,:]),3,(163,50,204),-1)
                            cv2.circle(frame, (cx,cy), 3, (0,0,255), -1)
                            cv2.drawContours(frame,[approx],0,(0,255,0),1)

                            calc = True
    
                        except Exception as e:
                            calc = False
                            print e

                    # Operations on the frame
                    skin = cv2.bitwise_and(frame, frame, mask = skinMask)
                    if len(contours) > 0 and calc:
                        cv2.circle(skin, (cx,cy), 3, (0,0,255))

                    skin=cv2.flip(skin,1)
                    cv2.imshow('Filtered Frame',skin)

                # Display frame in a window
                cv2.imshow('Frame',frame)
                #cv2.imshow('mask',skinMask)
                interrupt=cv2.waitKey(1)
                # Quit by pressing 'q'
                if  interrupt & 0xFF == ord('q'):
                    break

  #rospy.init_node('luko_cv', anonymous = True)
    #rate = rospy.Rate(1)
    #while not rospy.is_shutdown():
            #hello_str = "hello world %s" % rospy.get_time()
            #rospy.loginfo(hello_str)
            #pub.publish(hello_str)
            #rate.sleep()

if __name__ == '__main__':
    rospy.init_node('luko_cv', anonymous = True)
    vision = cv()
    try:
        vision.run()
    except KeyboardInterrupt, TypeError:
         camera.release()
         cv2.destroyAllWindows()

#try:
 #   while(1):
  #      calc = False
       
#except KeyboardInterrupt, TypeError:
 #   # Release camera & end program
