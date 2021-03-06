#!/usr/bin/env python
import json
import rospy
import operator
import sys
import numpy as np
from sensor_msgs.msg import JointState
from mbed_interface.msg import JointAngles
from std_msgs.msg import String

class playback:
    def __init__(self):
        self.sub = rospy.Subscriber("mbed/joint_states", JointState, self.callback, queue_size=10)
        self.pub = rospy.Publisher("mbed/set_target_angle", JointAngles, queue_size=10)
        
        self.pub_action = rospy.Subscriber("playback/action", String, self.callback_action, queue_size = 10)
        self.moved = False # move flag 
        self.ref = [70,75,40,50,75]
        self.path = [] 
        self.speed = 40 # default 20hz

    def callback(self, ros_data):
        self.ref = np.array(map(int, ros_data.position))
        s = "Reference = "
        for i in self.ref:
            s += str(int(i)) + " "
        print s 
 
    def callback_action(self, data):
        # Rewritten with np arrays, because fuck functional programming
        action = data.data
        read_mask = False
        temp = []
        mask = np.array([1,1,1,1,1])
        with open(action) as f:
            for line in f:
                if not read_mask:
                    self.mask = np.array(json.loads(line))
                    read_mask = True
                    for i,flag in enumerate(self.mask):
                        print "[Action=%s] Joint %d " % (action, i+1) + ("active" if flag else "inactive")
                else:
                    # because this is much easier to read and understand
                    deltas = np.array(map(int,line.split()),dtype=np.int16) # loads delta from line
                    point = np.array(map(operator.mul,deltas,mask)) + self.ref   # <delta,mask> + base_point
                    print "point from file: " + str(point)
                    temp.append(point)

        # Start with first point
        self.path = []
        self.path.append(temp[0])
        # Interpolate between each listed point
        for i in range(1,len(temp)):
            mid = (temp[i] + temp[i-1])/2
            self.path.append(mid)
            self.path.append(temp[i])
        self.moved = False

    def run(self):
        print "Playback is running"
        r = rospy.Rate(self.speed) #20hz - same as recording
        while not rospy.is_shutdown():
            if not self.moved:
                for point in self.path:
                    msg = JointAngles()
                    msg.joints = list(point)
                    self.pub.publish(msg)
                    r.sleep()
                self.moved = True
            
                print "Performed action"

    def runOnce(self,action):
        # Rewritten with np arrays, because fuck functional programming
        read_mask = False
        temp = []
        mask = np.array([1,1,1,1,1])
        r = rospy.Rate(self.speed)
        with open(action) as f:
            for line in f:
                if not read_mask:
                    self.mask = np.array(json.loads(line))
                    read_mask = True
                    for i,flag in enumerate(self.mask):
                        print "[Action=%s] Joint %d " % (action, i+1) + ("active" if flag else "inactive")
                else:
                    # because this is much easier to read and understand
                    deltas = np.array(map(int,line.split()),dtype=np.int16) # loads delta from line
                    point = np.array(map(operator.mul,deltas,mask)) + self.ref   # <delta,mask> + base_point
                    print "point from file: " + str(point)
                    temp.append(point)

        # Start with first point
        msg = JointAngles()
        msg.joints = list(temp[0])
        self.pub.publish(msg)
        r.sleep() 
        # Interpolate between each listed point
        for i in range(1,len(temp)):
            mid = (temp[i] + temp[i-1])/2
            msg.joints = list(mid)
            self.pub.publish(msg)
            r.sleep()
          
            msg.joints = temp[i]
            self.pub.publish(msg)
            r.sleep()

        print "Performed action: " + action


if __name__ == '__main__':
    rospy.init_node('playback', anonymous=True)
    try:
        playback = playback()
        #playback.run()
        playback.runOnce(sys.argv[1])
    except rospy.ROSInterruptException:
        pass
            
         
        
