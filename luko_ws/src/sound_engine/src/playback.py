#!/usr/bin/env python
import json
import rospy
import operator
import sys
import numpy as np
from sensor_msgs.msg import JointState
from mbed_interface.msg import JointAngles

class playback:
    def __init__(self):
        self.sub = rospy.Subscriber("mbed/joint_states", JointState, self.callback, queue_size=10)
        self.pub = rospy.Publisher("mbed/set_target_angle", JointAngles, queue_size=10)
        self.ref = []
        self.path = [] 
        self.mask = [1,1,1,1,1]
	print "Playing back..."

    def callback(self, ros_data):
        if not self.ref:
            self.ref = map(int, ros_data.position)
            s = "Reference = "
            for i in self.ref:
                s += str(int(i)) + " "
            print s 
 
    def run(self, filename):
        r = rospy.Rate(20) #20hz - same as recording
        while not self.ref:
            pass #wait for reference angle
        with open(filename) as f:
            read_mask = False
            for line in f:
                if not read_mask:
                    # Getting mask for joints, defined as the first line of recording.txt
                    self.mask = json.loads(line)
                    read_mask = True
                    for i,flag in enumerate(self.mask):
                        print "Joint %d: " % (i+1) + ("active" if flag else "inactive")
                else:
                    #msg = JointAngles()
                    joints = map(int, line.split())
                    #print joints
                    new_joints = map(operator.add, map(operator.mul,joints,self.mask), self.ref)
                    #msg.joints = new_joints
                    #self.pub.publish(msg)
                    #print msg
                    #r.sleep()

                    # Storing target points into a list first
                    self.path.append(np.array(new_joints,dtype = np.int16))

           # Publish first point of the path
        msg = JointAngles()
        msg.joints = list(self.path[0])
        self.pub.publish(msg)
        r.sleep()

        for i in range(1,len(self.path)):
            # midpoint interpolation
            mid = (self.path[i] + self.path[i-1])/2
            msg.joints = list(mid)
            print msg.joints
            self.pub.publish(msg)
            r.sleep()

            msg.joints = list(self.path[i])
            print msg.joints
            self.pub.publish(msg)
            r.sleep()              
 

                #print joints
                #new_joints = map(operator.add, map(operator.mul,joints,self.mask), self.ref)
                #msg.joints = new_joints
                #self.pub.publish(msg)
                #print msg
                #r.sleep()
 

        print "Done!"

if __name__ == '__main__':
    rospy.init_node('playback', anonymous=True)
    playback = playback()
    try:    
        playback.run(sys.argv[1])
    except rospy.ROSInterruptException:
        pass
            
         
        
