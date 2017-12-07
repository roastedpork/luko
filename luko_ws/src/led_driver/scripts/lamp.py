#!/usr/bin/env python

from led_driver.msg import LedArray
from led_driver.msg import Light
from speech_recognition.msg import Intent 
import numpy as np
import rospy
import colorsys

import json

VEL = 0.2
RATE = 30
LIGHT_HUE = 0.05

defBright = 5
defWarmth = 5
targBright = defBright
targWarmth = defWarmth

def clamp(val, mini, maxi):
    return min(max(val,mini),maxi)

def getLightValue(warmth, brightness):
    return (np.array(colorsys.hsv_to_rgb(LIGHT_HUE, warmth/10.0, brightness/10.0))*255).astype('int')

def setTarget(data):
    global targBright
    global targWarmth
    targBright = int(data.bright)
    targWarmth = int(data.warm)

def pubLight(warmth, brightness):
    msg = Light()
    msg.bright = brightness
    msg.warm = warmth
    pub_light.publish(msg)

def setLight(warmth, brightness):
    msg = LedArray()
    msg.op = 'fill'
    rgb = getLightValue(warmth, brightness)
    msg.r = [rgb[0]]
    msg.g = [rgb[1]]
    msg.b = [rgb[2]]
    pub_image.publish(msg)

def parseLight(intent):

    act = intent.action
    params = json.loads(intent.params)
    if (act == 'brightness'):
        val = params['number']
        if val == '':
            val = 2
        else:
            val = int(val)
        relative = params['relative_brightness']
        brightness = 0
        if len(relative)==0:
            brightness = clamp(val,0,10)
        else:
            brightness = clamp(targBright+int(relative[0])*val,0,10)
        pubLight(targWarmth,clamp(brightness,0,10))
    elif (act == 'warmth'):
        val = 0
        relative = params['relative']
        if len(params['number']) == 0:
            val = 2
            relative = 1
        else:
            val = int(params['number'][0])
        relativew = params['relative_warmth']
        warmness = 0
        if not relative:
            warmness = clamp(val,0,10)
        else:
            warmness = clamp(targWarmth+int(relativew[0])*val,0,10)
        pubLight(clamp(warmness,0,10),targBright)
    elif (act == 'color'):
        print 'col'
    else :
        print 'def'


pub_image = rospy.Publisher("send_image",LedArray,queue_size = 10)
pub_light = rospy.Publisher("set_light",Light, queue_size = 10)
sub_light = rospy.Subscriber("set_light",Light, setTarget, queue_size = 10)
sub_intent = rospy.Subscriber("intent/light",Intent, parseLight, queue_size = 10)

currBright = targBright
currWarmth = targWarmth

rospy.init_node('colour_sender', anonymous = True)
r = rospy.Rate(RATE)
setLight(currWarmth, currBright)

while not rospy.is_shutdown():
    warmDiff = targWarmth-currWarmth
    brightDiff = targBright-currBright
    if(abs(warmDiff) > VEL or abs(brightDiff) > VEL):
        if(warmDiff>0):
            currWarmth += VEL
        elif(warmDiff<0):
            currWarmth -= VEL

        if(brightDiff>0):
            currBright += VEL
        elif(brightDiff<0):
            currBright -= VEL
        setLight(currWarmth, currBright)
    else :
        currWarmth = targWarmth
        currBright = targBright
    r.sleep()


