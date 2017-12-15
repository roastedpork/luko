#!/usr/bin/env python
import rospy
import random
from mbed_interface.msg import JointAngles
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

def talker():
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('joint_state_publisher')
#    rospy.init_node('Recv_From_mbed', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    msg = JointState()

    while not rospy.is_shutdown():
	msg.header = Header()
        msg.header.stamp = rospy.Time.now()
	msg.name = ['cylinder_joint', 'low_joint0', 'low_joint1', 'low_joint2', 'up_joint0', 'up_joint1', 'up_joint2', 'head_bearing_link', 'head_to_lamp']
	msg.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
