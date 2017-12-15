#!/usr/bin/env python

import rospy
from speech_recognition.msg import Intent
from std_msgs.msg import String

import sys
import numpy as np
import collections
from mic_array import MicArray
from pixel_ring import pixel_ring
from snowboydetect import SnowboyDetect
from collections import deque
import audioop
import math
import wave
import pyaudio

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import apiai
import json
import unicodedata
from time import time

RATE = 16000
CHANNELS = 8
KWS_FRAMES = 10     # ms
DOA_FRAMES = 800    # ms

THRESH_SPEECH = 4400
THRESH_SILENCE = 4400

LISTEN_TIMEOUT = 5.0
MIN_RECORD_TIME = 1.5
MAX_RECORD_TIME = 8.0

DF_ACCESS_TOKEN = "82e816725d8b41c0aae0248eb1116e67"


class speech_recognition:


    def __init__(self):
        self.pub = {
                'generic' : rospy.Publisher("intent/generic", Intent, queue_size=10),
                'smalltalk' : rospy.Publisher("intent/smalltalk", Intent, queue_size=10),
                'light' : rospy.Publisher("intent/light", Intent, queue_size=10),
                'movement' : rospy.Publisher("intent/movement", Intent, queue_size=10),
                'player' : rospy.Publisher("intent/player", Intent, queue_size=10),
                'project' : rospy.Publisher("search_images/query", Intent, queue_size=10)
                }

        self.detector = SnowboyDetect('snowboy/resources/common.res', 'speech_recognition/src/hey_luko.pmdl')
        self.detector.SetAudioGain(0.5)
        self.detector.SetSensitivity('0.5')

        self.client = speech.SpeechClient()
        self.config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code='en-US')

        self.ai = apiai.ApiAI(DF_ACCESS_TOKEN)

    def queryDialogflow(self,query):
        request = self.ai.text_request()
        request.session_id = 1
        request.query = query
        return request.getresponse()



    def processResponse(self, query):
        response = self.queryDialogflow(query).read()
        res_json = json.loads(' '.join(response.split()))
        return res_json['result']['action'], res_json['result']['parameters']


    def filterPublish(self, action, params):
        msg = Intent()
        topic = action.split('.',1)
        msg.action = topic[1]
        msg.params = json.dumps(params)
        publisher = self.pub.get(topic[0],self.pub['generic'])
        publisher.publish(msg)
        if topic != "project":
            clearMsg = Intent()
            clearMsg.action = "clear_image"
            self.pub["project"].publish(clearMsg)

    def hotwordCallback(self, mic, doa):

        started = False
        rel = RATE/1024
        slide_win = deque(maxlen=4 * rel)
        frames = []

        timeStart = time()
        timeSpeak = 9999999999999.9

        for chunk in mic.read_chunks():
            slide_win.append(math.sqrt(abs(audioop.avg(chunk,4))))
            speechConf = sum([x > THRESH_SPEECH for x in slide_win])
            silenceConf = sum([x > THRESH_SILENCE for x in slide_win])
            utteredFrames = []
            currTime = time()
            if not started and speechConf > 0:
                print("started")
                started = True
                timeSpeak = time()
            elif not started and (currTime-timeStart) > LISTEN_TIMEOUT:

                self.filterPublish("generic.unknown","")
                print("Silent for too long, returning")
                return
            elif (started and (silenceConf == 0) and (currTime-timeSpeak)>MIN_RECORD_TIME) \
                    or ((currTime-timeSpeak) > MAX_RECORD_TIME):
                print("stopped\n")
                started = False
                recording = b''.join(frames)
                audio = types.RecognitionAudio(content=recording)
                pixel_ring.set_color(rgb=0x000010)
                print "recognising"
                response = self.client.recognize(self.config, audio)
                print "received response"
                transcript = '';
                for result in response.results:
                    transcript = result.alternatives[0].transcript
                    print('Transcript:{}'.format(transcript))
                if transcript != '':
                    action, params= self.processResponse(transcript)
                    print "actions: {}".format(json.dumps(action))
                    if params != '{}':
                        print "params: \n{}".format(json.dumps(params))
                    self.filterPublish(action,params)
                else:
                    print("speech recognition cannot recognise speech")
                    self.filterPublish("generic.unknown","")
                return
            else:
                frames.append(chunk[0::CHANNELS].tostring())
                #suppress_chunk = mic.suppress_noise(chunk, doa)
                #frames.append(suppress_chunk.tostring())
    def run(self):
        r = rospy.Rate(10)

        while not rospy.is_shutdown():

            history = collections.deque(maxlen=int(DOA_FRAMES / KWS_FRAMES))
            try:
                with MicArray(RATE, CHANNELS, RATE * KWS_FRAMES / 1000)  as mic:
                    for chunk in mic.read_chunks():
                        history.append(chunk)

                        # Detect keyword from channel 0
                        ans = self.detector.RunDetection(chunk[0::CHANNELS].tostring())
                        if ans > 0:
                            msg = Intent()
                            msg.action = 'hey_luko'
                            self.pub['generic'].publish(msg)
                            frames = np.concatenate(history)
                            direction = mic.get_direction(frames)
                            pixel_ring.set_direction(direction)
                            print('Hotword detected \n{}'.format(int(direction)))
                            self.hotwordCallback(mic, int(direction));
                            pixel_ring.off()
            except:
                raise

        pixel_ring.off()






if __name__ == '__main__':
    rospy.init_node('speech_recognition', anonymous=True)
    speech = speech_recognition()
    speech.run()
