#!/usr/bin/env python
import rospy
import numpy as np
import serial
from mbed_interface.msg import JointAngles
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

hex = lambda x : '0'<=x<='9' or 'a'<=x<='f'

class mbed_interface:
    def __init__(self):
        #self.pub = rospy.Publisher("mbed/get_current_angle",JointAngles, queue_size=10)
        self.pub = rospy.Publisher("mbed/joint_states",JointState, queue_size=10)
        self.sub = rospy.Subscriber("mbed/set_target_angle", JointAngles, self.callback, queue_size=10)
	self.serial = serial.Serial(
            port="/dev/ttyACM0",
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
	print "Serial Connection: "+ str(self.serial.isOpen())
	self.serial.flushInput()
	self.serial.flushOutput()

    def readSerialIn(self,str):
        try:
            strip = "".join([c for c in str if hex(c)])
            res = [int(strip[i:i+2],16) for i in range(0,10,2)]
        except Exception as e:
            print e
            res = [0.0, 0.0, 0.0, 0.0, 0.0]
        return res

    def callback(self,ros_data):
           
            ### read target_angle msg from callback ###
            target = [int(round(np.degrees(j))) for j in ros_data.joints]
            target[0] = target[0]+66
            target[1] = target[1]+50
            target[2] = target[2]+60
            target[3] = target[3]+65
            target[4] = target[4]+86
	    rospy.loginfo("New target: " + ", ".join([str(i) for i in target]))
            msg = '<' + ''.join([format(j,'02x') for j in target]) + '>'
            self.serial.write(msg)
            rospy.loginfo(msg)
    def run(self):
        r = rospy.Rate(10)

        while not rospy.is_shutdown():
            ### create current_angle msg and publish ###
            readout = self.serial.readline()

            msg = JointState()
            joints = self.readSerialIn(self.serial.readline())
            self.serial.flushInput() # we want to get the latest values
	    
            msg.header = Header()
            msg.header.stamp = rospy.Time.now()
            msg.name = ['cylinder_joint', 'low_joint0', 'low_joint1', 'low_joint2', 'up_joint0', 'up_joint1', 'up_joint2', 'head_bearing_link', 'head_to_lamp']
            msg.position = [joints[0], joints[1], joints[1], -joints[1], joints[2], joints[2], -joints[2], joints[3], joints[4]]
            #rospy.loginfo('[' + ", ".join([str(i) for i in msg.position]) + ']' )
            self.pub.publish(msg)
	    r.sleep()


if __name__ == '__main__':
    rospy.init_node('mbed_Interface', anonymous=True)
    mbed = mbed_interface()    
    try:
        mbed.run()
    except rospy.ROSInterruptException:
        pass
