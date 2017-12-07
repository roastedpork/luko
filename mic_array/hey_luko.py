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
from time import time

RATE = 16000
CHANNELS = 8
KWS_FRAMES = 10     # ms
DOA_FRAMES = 800    # ms

THRESH_SPEECH = 3900
THRESH_SILENCE = 3700

DF_ACCESS_TOKEN = "82e816725d8b41c0aae0248eb1116e67"

detector = SnowboyDetect('snowboy/resources/common.res', 'hey_luko.pmdl')
detector.SetAudioGain(1)
detector.SetSensitivity('0.5')

client = speech.SpeechClient()
config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en-US')

ai = apiai.ApiAI(DF_ACCESS_TOKEN)

def queryDialogflow(query):
    request = ai.text_request()
    request.session_id = 1
    request.query = query
    return request.getresponse()



def processResponse(query):
    response = queryDialogflow(query).read()
    res_json = json.loads(' '.join(response.split()))
    return res_json['result']['action'], res_json['result']['parameters']

LISTEN_TIMEOUT = 5.0
MIN_RECORD_TIME = 1.5
MAX_RECORD_TIME = 8.0

def hotwordCallback(mic, doa):

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
            print("Silent for too long, returning")
            return
        elif (started and (silenceConf == 0) and (currTime-timeSpeak)>MIN_RECORD_TIME) \
                or ((currTime-timeSpeak) > MAX_RECORD_TIME):
            print("stopped\n")
            started = False
            #recording = b''.join(frames)
            #wf = wave.open("supress_out.wav",'wb')
            #wf.setnchannels(1)
            #wf.setsampwidth(2)
            #wf.setframerate(RATE)
            #wf.writeframes(recording)
            #wf.close()
            #return
            recording = b''.join(frames)
            audio = types.RecognitionAudio(content=recording)
            print "recognising"
            response = client.recognize(config, audio)
            print "received response"
            transcript = '';
            for result in response.results:
                transcript = result.alternatives[0].transcript
                #print('Transcript:{}'.format(result.alternatives[0].transcript))
                print('Transcript:{}'.format(transcript))
            if transcript != '':
                action, params= processResponse(transcript)
                print "actions: {}".format(json.dumps(action))
                if params != '{}':
                    print "params: \n{}".format(json.dumps(params))
            #wf = wave.open("output.wav", 'wb')
            #wf.setnchannels(2)
            #wf.setsampwidth(mic.chunk_size)
            #wf.setframerate(RATE)
            #wf.writeframes(b''.join(utteredFrames))
            #wf.close()

            return
        else:
            suppress_chunk = mic.suppress_noise(chunk, doa)
            frames.append(suppress_chunk.tostring())
            #frames.append(chunk[0::CHANNELS].tostring())

 #           if (sum(x>THRESH) > 0):
 #               if not started:
 #                   print("Start speaking")
 #                   started = True
 #           elif started is True:
 #               print("done")
 #               break
        #for x in slid_win:

            #if x > 4500:
            #    print(x)



def main():

    history = collections.deque(maxlen=int(DOA_FRAMES / KWS_FRAMES))

    try:
        with MicArray(RATE, CHANNELS, RATE * KWS_FRAMES / 1000)  as mic:
            for chunk in mic.read_chunks():
                history.append(chunk)

                # Detect keyword from channel 0
                ans = detector.RunDetection(chunk[0::CHANNELS].tostring())
                if ans > 0:
                    frames = np.concatenate(history)
                    direction = mic.get_direction(frames)
                    pixel_ring.set_direction(direction)
                    print('Hotword detected \n{}'.format(int(direction)))
                    hotwordCallback(mic, int(direction));

    except KeyboardInterrupt:
        pass

    pixel_ring.off()


if __name__ == '__main__':
    main()
