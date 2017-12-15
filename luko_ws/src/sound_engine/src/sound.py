#!/usr/bin/env python
# sound.py
# Contains mapping of Dialogflow Intents to WAV files and sample rates and a play function that randomises sample rate slightly

import array
from random import randint
import os
from subprocess import Popen
import numpy as np
from pydub import AudioSegment
import time
from playback import playback

import rospy
from speech_recognition.msg import Intent
from mbed_interface.msg import JointAngles

intent_map = {
        'hey_luko'            : ['hey', 4],
        'unknown'             : ['unknown', 4],
        #'agent.acquaintance'  : ['acq', 4],
        #'agent.age'           : ['age', 4],
        #'agent.birth\_date'   : ['dob', 4],
        #'agent.busy'          : ['busy', 4],
        #'agent.can\_you\_help': ['help', 3],
        #'agent.chatbot'       : ['chatbot', 5],
        #'agent.hungry'        : ['hungry', 6],
        'agent.marry_user'   : ['marry', 3],
        #'agent.my\_friend'    : ['friend', 3],
        'dialog.how_are_you': ['hay', 4],
        #'agent.real'          : ['real', 3],
        #'agent.there'         : ['there', 4],
        'appraisal.good'      : ['good', 2],
        'appraisal.no_problem': ['np', 3],
        'appraisal.thank_you': ['thx', 3],
        'appraisal.well_done': ['wd', 2],
        'appraisal.welcome'   : ['welcome', 3],
        'dialog.i_do_not_care': ['idc', 5],
        'dialog.sorry'        : ['sorry', 3],
        'dialog.what_do_you_mean': ['wdym', 4],
        #'dialog.wrong'        : ['wrong', 5],
        #'emotions.ha_ha'     : ['haha', 2],
        'emotions.wow'        : ['wow', 3],
        'greetings.bye'       : ['bye', 3],
        #'greetings.goodevening': ['ge', 4],
        #'greetings.goodmorning': ['gm', 4],
        #'greetings.goodnight' : ['gn', 3],
        'greetings.hello'     : ['hello', 4],
        'greetings.how_are_you': ['hay', 4],
        'greetings.nice_to_meet_you': ['ntmy', 3],
        'greetings.nice_to_talk_to_you': ['nttty', 3],
        'greetings.whatsup'   : ['whatsup', 3],
        'user.bored'          : ['bored', 5],
        'user.happy'          : ['happy', 3],
        'user.sad'            : ['sad', 6],
        'user.tired'            : ['sad', 6],
        #'user.sleepy'         : ['sleepy', 5],
        'user.testing_agent' : ['u', 2],
        'test_intent'         : ['a', 3],
        'default'             : ['e', 3]
    }

class SoundEngine:
    def __init__(self):
        # initialize pubsub topics
        self.sub_smalltalk = rospy.Subscriber("intent/smalltalk", Intent, self.callback, queue_size = 10)
        self.sub_generic = rospy.Subscriber("intent/generic", Intent, self.callback, queue_size = 10)
        self.pub_joints = rospy.Publisher("mbed/set_target_angle", JointAngles, queue_size = 10)
        #self.pub_action = rospy.Publisher("playback/action", JointAngles, queue_size = 10)

    def callback(self,intent):

        action = intent.action
        print action
        try:
            audio_file = intent_map[action][0]
            rate = intent_map[action][1] + (randint(-9,9)/10.0)
        except KeyError:
            audio_file = intent_map["default"][0]
            rate = intent_map["default"][1] + (randint(-9,9)/10.0)

        song = AudioSegment.from_wav("/home/pi/luko/luko_ws/src/sound_engine/src/sounds/" + audio_file + ".wav")

        samples = song.get_array_of_samples()

        sampled = np.delete(samples, np.arange(0, len(samples), rate))

        result = song._spawn(array.array(song.array_type, sampled))

        filename = "luko_sound_" + str(time.time()) + ".wav"

        result.export(filename, format="wav")

        # Playback action
        msg = JointAngles()
        if action == 'hey_luko':
            msg.joints = [75,75,40,20,75]
            self.pub_joints.publish(msg)
        elif action == 'unknown':
            msg.joints = [75,75,40,50,75]
            self.pub_joints.publish(msg)
        else:
            action_file = "actions/" + audio_file + ".txt"
            Popen(["python", "playback.py", action_file])
            time.sleep(1.5)

        # Play generated sound file and then delete the file
        os.system("aplay " + filename)
        os.remove(filename)

        # Return to idle
        if action != 'hey_luko' and action != 'unknown':
            time.sleep(2)
            msg.joints = [75,75,40,50,75]
            self.pub_joints.publish(msg)

if __name__ == '__main__':

    sound = SoundEngine()
    rospy.init_node('SoundEngine', anonymous=True)
    rospy.loginfo('Listening for smalltalk...')
    rospy.spin()
