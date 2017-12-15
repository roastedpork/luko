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
import json
from imagehandler import ImageHandler
from std_msgs.msg import String, Bool
from speech_recognition.msg import Intent
from mbed_interface.msg import JointAngles
from sensor_msgs.msg import JointState

# dimension of the display
screen_cols = 624 #1920 #1182
screen_rows = 1182 #1080 #624



class ScreenHandler(object):
    def __init__(self):
        # initialize GUI environment
        pygame.init()
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.NOFRAME | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((screen_cols,screen_rows), flags)
        self.screen.fill([0,0,0])
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Luko")

        # initialize state variables
        self.clock = pygame.time.Clock()
        self.info = pygame.display.Info()
        self.image = ImageHandler('/home/pi/searchRes/cat_04.jpg')
        self.rot =  0
        self.theta = 0

        # initialize pubsub topics
        #self.sub_request = rospy.Subscriber("search_images/query", Intent, self.callback_request, queue_size = 10)
        self.sub_status = rospy.Subscriber("search_images/status_flag", Intent, self.callback_status, queue_size = 10)
        self.sub_angles = rospy.Subscriber("mbed/joint_states", JointState, self.callback_angles, queue_size = 10)
        self.query = None
        self.readings_rot = [0,0,0,0,0,0,0,0,0,0]
        self.readings_theta = [0,0,0,0,0,0,0,0,0,0]
        self.index_rot = 0
        self.index_theta = 0

    def callback_request(self,data):
        params = json.loads(data.params)
        print params
        if data.action == 'image':
            self.query = " ".join(params['image']) + ("" if params['no_blk'] == "1" else ' black background')
            print "New query: " + self.query
        elif data.action == 'clear_image':
            self.image = None

    def callback_status(self,data):
        print 'Ready to load image'
        exts = ['.jpg','.jpeg','.png','.gif']
        p = json.loads(data.params)
        if p:
            ind = random.randint(0,4)
            filepath = ['/home/pi/searchRes/' + p['prefix'] + '_%02d' %(ind) + ext for ext in exts]
            for file in filepath:
                try:
                    temp = ImageHandler(file)
                    self.image = temp
                except:
                    pass

    def callback_angles(self,data):
        # subscribed to "mbed/get_current_angles" topic
        self.readings_rot[self.index_rot] = data.position[0]-70
        self.index_rot = (self.index_rot+1)%3
        self.rot = sum(self.readings_rot)/3.0
        self.readings_theta[self.index_theta] = 57-data.position[3]
        self.index__theta = (self.index_theta+1)%3
        self.theta = sum(self.readings_theta)/3.0
        
    def run(self):
        r = rospy.Rate(30)
        try:
            while not rospy.is_shutdown():
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        sys.exit(0)
                    rospy.loginfo(event)

                self.screen.fill([0,0,0])                    
                if self.image is not None:
                    try:
                        self.image.rotate(self.rot)
                        self.image.transform(self.theta)
                        self.image.display(self.screen)
                    except Exception as e:
                        print e
                pygame.display.update()

                #self.theta = self.theta+3 if self.theta < 87 else 0
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

