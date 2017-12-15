#!/usr/bin/env python

from PIL import Image
import numpy as np
from led_driver.msg import LedArray
import rospy
from std_msgs.msg import String

class bmp2led:

    def __init__(self):
        self.sub_image = rospy.Subscriber("display_image", String, self.callback, queue_size = 1)
        self.pub_image = rospy.Publisher('send_image', LedArray, queue_size=10)

    def bmp2rgb_andrew(self,img_file):
        img = Image.open(img_file)
        rgb_im = img.convert('RGB')

        arr = np.array(rgb_im)
        nw_arr = arr[1:]

        [r_raw,g_raw,b_raw] = np.dsplit(nw_arr,nw_arr.shape[-1])

        r_flat = r_raw.flatten()
        g_flat = g_raw.flatten()
        b_flat = b_raw.flatten()
        size = r_flat.size

        r = np.delete(r_flat, [0,8,size-18,size-10,size-9,size-8,size-2,size-1])
        g = np.delete(g_flat, [0,8,size-18,size-10,size-9,size-8,size-2,size-1])
        b = np.delete(b_flat, [0,8,size-18,size-10,size-9,size-8,size-2,size-1])

        return r,g,b
    
    def bmp2rgb(self,img_file):
        img = Image.open(img_file)
        rgb_im = img.convert('RGB')

        arr = np.array(rgb_im)

        [r_raw,g_raw,b_raw] = np.dsplit(arr,arr.shape[-1])

        r = r_raw.flatten()
        g = g_raw.flatten()
        b = b_raw.flatten()

        return r,g,b

    def callback(self,image):
        img = image.data

        try:
            img_file = "bmps/" + img + ".bmp"
            msg = LedArray()
            msg.op = 'raw'
            msg.nPixels = 64
            msg.r,msg.g,msg.b = self.bmp2rgb(img_file)
            self.pub_image.publish(msg)
        except:
            pass

if __name__ == "__main__":
    bmp = bmp2led()
    rospy.init_node('bmp2led', anonymous=True)
    rospy.loginfo('Listening for image strings...')
    rospy.spin()
