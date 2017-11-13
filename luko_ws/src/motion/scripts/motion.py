#!/usr/bin/env python
# license removed for brevity
import rospy
import random
from mbed_interface.msg import JointAngles

def talker():
    pub = rospy.Publisher('mbed/set_target_angle', JointAngles, queue_size=10)
    rospy.init_node('IK_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
	msg = JointAngles()
	msg.joints = [random.randint(0,100) for i in range(5)]
        rospy.loginfo("Sending: "+ str(msg.joints))
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
