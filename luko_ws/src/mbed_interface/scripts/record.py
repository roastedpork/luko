#!/usr/bin/env python
import sys
import rospy
import operator
from sensor_msgs.msg import JointState

try:
    flags=[int(i) for i in sys.argv[1:]]
    filename = "recording.txt"
except:
    filename = sys.argv[1]
    flags=[int(i) for i in sys.argv[2:]]

class record:
    def __init__(self):
        self.sub = rospy.Subscriber("mbed/joint_states", JointState, self.callback, queue_size=10)
        self.file = open(filename, "w")
        self.ref = []
        self.file.write(str(flags)+ "\n")
	print "Recording..."

    def callback(self, ros_data):
        joints = ros_data.position
	if not self.ref:
            self.ref = joints
        joints_fil = map(operator.sub, joints, self.ref)
        for item in joints_fil:
            self.file.write(str(int(round(item))) + " ")
        self.file.write("\n")

    def run(self):
        while not rospy.is_shutdown():
            pass
    
if __name__ == '__main__':
    rospy.init_node('record', anonymous=True)
    record = record()
    try:    
        record.run()
    except rospy.ROSInterruptException:
        pass
            
         
        
