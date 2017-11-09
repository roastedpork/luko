#!/usr/bin/env python
import rospy
import serial
from mbed_interface.msg import JointAngles

hex = lambda x : '0'<=x<='9' or 'a'<=x<='f'

class mbed_interface:
    def __init__(self):
        self.pub = rospy.Publisher("mbed/get_current_angle",JointAngles, queue_size=10)
        self.sub = rospy.Subscriber("mbed/set_target_angle", JointAngles, self.callback, queue_size=10)
	self.serial = serial.Serial(
            port="/dev/ttyAMA0",
            baudrate=9600,
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
        except:
            res = []
        return res

    def callback(self,ros_data):
	   rospy.loginfo("New target: " + ", ".join([str(i) for i in ros_data.joints]))
           
           ### read target_angle msg from callback ###
           target = [int(round(j)) for j in ros_data.joints]
           msg = '<' + ''.join([format(j,'02x') for j in target]) + '>'
           self.serial.write(msg)
           
    def run(self):
        r = rospy.Rate(10)

        while not rospy.is_shutdown():
            ### create current_angle msg and publish ###
            readout = self.serial.readline()

            msg = JointAngles()
            msg.joints = self.readSerialIn(self.serial.readline())
            self.serial.flushInput() # we want to get the latest values
	    rospy.loginfo("Current: " + ", ".join([str(i) for i in msg.joints]))
            self.pub.publish(msg)
	    r.sleep()


if __name__ == '__main__':
    rospy.init_node('mbed_Interface', anonymous=True)
    mbed = mbed_interface()    
    mbed.run()
