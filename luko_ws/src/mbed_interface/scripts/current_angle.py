#!/usr/bin/env python
import rospy
import random
from mbed_interface.msg import JointAngles

def talker():
    pub = rospy.Publisher('current_angle', JointAngles)
    rospy.init_node('Recv_From_mbed', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg = JointAngles()

    while not rospy.is_shutdown():
	msg.joints = [random.randint(0,180) for i in range(5)]
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
