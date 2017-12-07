#!/usr/bin/env python
# sound.py
# Contains mapping of Dialogflow Intents to WAV files and sample rates and a play function that randomises sample rate slightly

import array
from random import randint
import os
import numpy as np
from pydub import AudioSegment

import rospy
from speech_recognition.msg import Intent

intent_map = {
        'hey_luko'            : ['hey.wav', 4],
        'unknown'             : ['unknown.wav', 4],
        #'agent.acquaintance'  : ['acq.wav', 4],
        #'agent.age'           : ['age.wav', 4],
        #'agent.birth\_date'   : ['dob.wav', 4],
        #'agent.busy'          : ['busy.wav', 4],
        #'agent.can\_you\_help': ['help.wav', 3],
        #'agent.chatbot'       : ['chatbot.wav', 5],
        #'agent.hungry'        : ['hungry.wav', 6],
        'agent.marry_user'   : ['marry.wav', 3],
        #'agent.my\_friend'    : ['friend.wav', 3],
        'dialog.how_are_you': ['hay.wav', 4],
        #'agent.real'          : ['real.wav', 3],
        #'agent.there'         : ['there.wav', 4],
        'appraisal.good'      : ['good.wav', 2],
        'appraisal.no_problem': ['np.wav', 3],
        'appraisal.thank_you': ['thx.wav', 3],
        'appraisal.well_done': ['wd.wav', 2],
        'appraisal.welcome'   : ['welcome.wav', 3],
        'dialog.i_do_not_care': ['idc.wav', 5],
        'dialog.sorry'        : ['sorry.wav', 3],
        'dialog.what_do_you_mean': ['wdym.wav', 4],
        #'dialog.wrong'        : ['wrong.wav', 5],
        #'emotions.ha_ha'     : ['haha.wav', 2],
        'emotions.wow'        : ['wow.wav', 3],
        'greetings.bye'       : ['bye.wav', 3],
        #'greetings.goodevening': ['ge.wav', 4],
        #'greetings.goodmorning': ['gm.wav', 4],
        #'greetings.goodnight' : ['gn.wav', 3],
        'greetings.hello'     : ['hello.wav', 4],
        'greetings.how_are_you': ['hay.wav', 4],
        'greetings.nice_to_meet_you': ['ntmy.wav', 3],
        'greetings.nice_to_talk_to_you': ['nttty.wav', 3],
        'greetings.whatsup'   : ['whatsup.wav', 3],
        'user.bored'          : ['bored.wav', 5],
        'user.happy'          : ['happy.wav', 2],
        'user.sad'            : ['sad.wav', 6],
        'user.tired'            : ['sad.wav', 6],
        #'user.sleepy'         : ['sleepy.wav', 5],
        'user.testing_agent' : ['u.wav', 2],
        'test_intent'         : ['a.wav', 3],
        'default'             : ['e.wav', 3]
    }

class SoundEngine:
    def __init__(self):
        # initialize pubsub topics
        self.sub_smalltalk = rospy.Subscriber("intent/smalltalk", Intent, self.callback, queue_size = 1)
        self.sub_generic = rospy.Subscriber("intent/generic", Intent, self.callback, queue_size = 1)

    def callback(self,intent):
        
        action = intent.action
        print action
        try:
            audio_file = intent_map[action][0]
            rate = intent_map[action][1] + (randint(-9,9)/10.0)
        except KeyError:
            audio_file = intent_map["default"][0]
            rate = intent_map["default"][1] + (randint(-9,9)/10.0)

        song = AudioSegment.from_wav("sounds/" + audio_file)

        samples = song.get_array_of_samples()

        sampled = np.delete(samples, np.arange(0, len(samples), rate))

        result = song._spawn(array.array(song.array_type, sampled))

        filename = "luko_sound_" + str(rate) + ".wav"

        result.export(filename, format="wav")

        # Play generated sound file and then delete the file
        os.system("aplay " + filename)
        os.remove(filename)

if __name__ == '__main__':

    sound = SoundEngine()
    rospy.init_node('SoundEngine', anonymous=True)
    rospy.loginfo('Listening for smalltalk...')
    rospy.spin()
