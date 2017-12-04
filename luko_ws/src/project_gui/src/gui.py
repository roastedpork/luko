#!/usr/bin/env python
import os
import sys
import time
import math
import random
import numpy as np
import pygame
import cv2
import rospy
from imagehandler import ImageHandler
from std_msgs.msg import String, Bool
from mbed_interface.msg import JointAngles

# dimension of the display
screen_cols = 1920 #1182
screen_rows = 1080 #624



class ScreenHandler(object):
    def __init__(self):
        # initialize GUI environment
        pygame.init()
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE #| pygame.NOFRAME | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((screen_cols,screen_rows), flags)
        self.screen.fill([0,0,0])
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Luko")

        # initialize state variables
        self.clock = pygame.time.Clock()
        self.info = pygame.display.Info()
        self.image = None #ImageHandler('/home/pi/searchRes/dogs_black_background_04.jpg')
        self.rot =  0
        self.theta = 0

        # initialize pubsub topics
        self.sub_request = rospy.Subscriber("search_images/query", String, self.callback_request, queue_size = 1)
        self.sub_status = rospy.Subscriber("search_images/status_flag", Bool, self.callback_status, queue_size = 1)
        self.sub_angles = rospy.Subscriber("mbed/get_current_angle", JointAngles, self.callback_angles, queue_size = 1)
        self.query = None

    def callback_request(self,data):
        self.query = data.data

    def callback_status(self,data):
        exts = ['.jpg','.jpeg','.png','.gif']
        prefix = self.query.replace(' ','_')
        if data.data:
            ind = random.randint(0,4)
            filepath = ['/home/pi/searchRes/' + prefix + '_%02d' %(ind) + ext for ext in exts]
            for file in filepath:
                try:
                    temp = ImageHandler(file)
                    self.image = temp
                except:
                    pass

    def callback_angles(self,data):
        # subscribed to "mbed/get_current_angles" topic
        pass

    def run(self):
        r = rospy.Rate(30)
        try:
            while not rospy.is_shutdown():
                for event in pygame.event.get():
                    #if event.type == pygame.KEYDOWN:
                    #    sys.exit(0)
                    rospy.loginfo(event)

                self.screen.fill([0,0,0])                    
                if self.image is not None:
                    self.image.rotate(self.rot)
                    self.image.transform(self.theta)
                    self.image.display(self.screen)
                pygame.display.update()

                self.theta = self.theta+3 if self.theta < 87 else 0
                r.sleep()

        except KeyboardInterrupt, SystemExit:
            pygame.quit()
            cv2.destroyAllWindows()
        
if __name__ == "__main__":
    gui =  ScreenHandler()

    rospy.init_node('Projection_GUI', anonymous = True)
    rospy.loginfo('Running GUI display...')
    gui.run()
    rospy.loginfo('Terminating GUI display')
