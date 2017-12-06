#!/usr/bin/env python

from led_driver.msg import LightDriver
import numpy as np
import rospy

state = 4*np.array([[0,1,0],[-1,0,0],[0,0,1],[0,-1,0],[1,0,0],[0,0,-1]])

colour = np.array([100,0,0])

pub = rospy.Publisher("send_image",LedArray,queue_size = 10)


rospy.init_node('colour_sender', anonymous = True)
r = rospy.Rate(30)

while not rospy.is_shutdown():
    for delta in state:
        for _ in range(25):
            colour += delta
            order = LightDriver()
            order.op = 'fill'
            order.r = [colour[0]]
            order.g = [colour[1]]
            order.b = [colour[2]]
            pub.publish(order)
            r.sleep()
