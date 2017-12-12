#!/usr/bin/env python
import rospy
import operator
import sys
from sensor_msgs.msg import JointState
from mbed_interface.msg import JointAngles

class playback:
    def __init__(self):
        self.sub = rospy.Subscriber("mbed/joint_states", JointState, self.callback, queue_size=10)
        self.pub = rospy.Publisher("mbed/set_target_angle", JointAngles, queue_size=10)
        self.ref = []
	print "Playing back..."

    def callback(self, ros_data):
        if not self.ref:
            self.ref = map(int, ros_data.position)
            s = "Reference = "
            for i in self.ref:
                s += str(int(i)) + " "
            print s 
 
    def run(self, filename):
        r = rospy.Rate(10) #10hz - same as recording
        while not self.ref:
            pass #wait for reference angle
        with open(filename) as f:
            for line in f:
                msg = JointAngles()
                joints = map(int, line.split())
                print joints
                new_joints = map(operator.add, joints, self.ref)
                msg.joints = new_joints
                self.pub.publish(msg)
                print msg
                r.sleep()
        print "Done!"

if __name__ == '__main__':
    rospy.init_node('playback', anonymous=True)
    playback = playback()
    try:    
        playback.run(sys.argv[1])
    except rospy.ROSInterruptException:
        pass
            
         
        
