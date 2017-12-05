#!/usr/bin/env python

from led_driver.msg import LightDriver
import rospy
import serial

### UART useable frequency is ~115200 bit/sec -> 1440 bytes/sec
### Each message has 5 bytes (compressed)
### ie. 2880 messages/sec
### Worst case: 90 messages to load a full image (89 pixels + 1 load instr)
### ie. 32hz update rate minimum

### Arduino will receive multiple "IRGB" (4 chars, 1 char/field) packets delimited by "\n"
### Each colour channel will receive 6 bits, shifted left 2 bits by the Arduino

### "I" field indicates index or instruction
### I = [0,88] denotes the location of the pixel value
### values I = [89,95] are for other instructions
### eg. updating the current buffer, turning the array dark quickly etc.


cmap = lambda x: chr(x+32) # accepts [0,95]
BUFFER_LOAD = 89
BUFFER_CLEAR = 90


class led_interface:
    def __init__(self):
        self.sub = rospy.Subscriber("send_image", LightDriver, self.callback, queue_size=10)
        self.serial = serial.Serial(
            port="/dev/ttyAMA0",
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        print "Serial Connection: "+ str(self.serial.isOpen())

    def callback(self,data):
        rospy.loginfo("Received Instruction: %s" %(data.op))
        
        if data.op == 'raw':
            msg_str = ''
            nPixels = data.nPixels
            msg_str += "%02x%02x%02x"% (int(data.r[0]),int(data.g[0]),int(data.b[0]))
            for i in range(1,nPixels):
                msg_str += " %02x%02x%02x"% (int(data.r[i]),int(data.g[i]),int(data.b[i]))
            msg_str += '\n'

        elif data.op == 'fill':
            msg_str = "# %02x%02x%02x\n"% (int(data.r[0]),int(data.g[0]),int(data.b[0]))

        rospy.loginfo(msg_str)
        self.serial.write(msg_str)
	
	

if __name__ == "__main__":
    driver = led_interface()
    rospy.init_node('led_driver_node', anonymous=True)

    rospy.spin()
