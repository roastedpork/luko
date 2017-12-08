#!/usr/bin/env python

import rospy
from cv.msg import Radial
from mbed_interface.msg import JointAngles
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils
import numpy as np
import math
import io

pixel_to_dist = 0.3
USER_DIST = 50
# Get user supplied values
cascPath = '/home/pi/luko/luko_ws/src/cv/src/haarcascade_frontalface_default.xml'#sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# initialize the camera and take reference to raw camera capture
camera = PiCamera()
camera.resolution = (160, 120)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(160, 120))

# allow camera to warm up
time.sleep(0.1)
lastTime = time.time()*1000.0
# capture frames from the camera


class cv:
    def __init__(self):
        self.pub = rospy.Publisher('mbed/set_target_angle', JointAngles, queue_size=10)

    def run(self):
        while not rospy.is_shutdown():
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                image = frame.array
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect faces in the image
                faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
                )
                print " Found {0} faces!".format(len(faces)) # time.time()*1000.0-lastTime,
                lastTime = time.time()*1000.0
                
                # Draw circle around face(s)
                for (x, y, w, h) in faces:
                    cx = x+w/2
                    cy = y+h/2
                    cv2.circle(image, (cx, cy), int((w+h)/3), (255, 255, 255), 1)
                    #msg = Radial()
                    #msg.radius = 57*np.arctan(pixel_to_dist*(cx-80)/USER_DIST)
                    #msg.theta =  57*np.arctan(pixel_to_dist*(cy-60)/USER_DIST)
                    msg = JointAngles()
                    msg.joints = [66.0, 50.0, 80.0,20+cy,60+cx]
                    self.pub.publish(msg)
               
               # show the frame
                cv2.imshow("Frame", image)
                key = cv2.waitKey(1) & 0xFF

                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break

if __name__ == '__main__':
    rospy.init_node('luko_cv', anonymous = True)
    vision = cv()
    vision.run()
