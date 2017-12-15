#!/usr/bin/env python
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import rospy

class luko_joint_loop:
    def __init__(self):
        self.pub = rospy.Publisher("/joint_states", JointState, queue_size=100)
        self.sub = rospy.Subscriber("/joint_states", JointState, self.update_position, queue_size=100)
        self.msg = JointState()
        self.msg.name = ['cylinder_joint', 'low_joint0', 'low_joint1', 'low_joint2', 'up_joint0', 'up_joint1', 'up_joint2', 'head_bearing_link', 'head_to_lamp']
                

    def run(self):
        self.msg.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        r = rospy.Rate(5)
        while not rospy.is_shutdown():
            self.msg.header = Header()
            self.msg.header.stamp = rospy.Time.now()  
            self.pub.publish(self.msg)
            r.sleep()
    
    def update_position(self, ros_data):
            self.msg.position = ros_data.position[:]

if __name__ == '__main__':
    rospy.init_node('luko_joint_loop', anonymous=True)
    node = luko_joint_loop();
    try:
        node.run()
    except rospy.ROSInterruptException:
        pass
    
