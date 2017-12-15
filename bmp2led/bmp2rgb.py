#!/usr/bin/env python

from PIL import Image
import numpy as np
from led_driver.msg import LedArray
import rospy

def bmp2rgb(img_file):
    img = Image.open("bmps/heart.bmp")
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

if __name__ == "__main__":
    rospy.init_node('bmp2led', anonymous=True)
    msg = LedArray()
    msg.op = 'raw'
    msg.nPixels = 64
    msg.r,msg.g,msg.b = bmp2rgb('bmps/heart.bmp')
    pub = rospy.Publisher('send_image', LedArray, queue_size=10)
    r = rospy.Rate(10)
    sent = False
    while not rospy.is_shutdown():
        pub.publish(msg)
        r.sleep()
        sent = True

        if sent:
            break
