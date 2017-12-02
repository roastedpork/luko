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

RATE = 16000
CHANNELS = 8
KWS_FRAMES = 10     # ms
DOA_FRAMES = 800    # ms

THRESH_SPEECH = 4000
THRESH_SILENCE = 3800

detector = SnowboyDetect('snowboy/resources/common.res', 'hey_luko.pmdl')
detector.SetAudioGain(1)
detector.SetSensitivity('0.5')

def hotwordCallback(mic):

    started = False
    rel = RATE/1024
    slide_win = deque(maxlen=4 * rel);
    mic.start()
    requests = None
    for chunk in mic.read_chunks():
        slide_win.append(math.sqrt(abs(audioop.avg(chunk,4))))
        speechConf = sum([x > THRESH_SPEECH for x in slide_win])
        silenceConf = sum([x > THRESH_SILENCE for x in slide_win])
        utteredFrames = [];

        if not started:
            if (speechConf > 0):
                print("started")
                started = True
        else:
            if(silenceConf > 0):
                print("-")
            else:
                print("stopped\n")
                started = False

                #wf = wave.open("output.wav", 'wb')
                #wf.setnchannels(2)
                #wf.setsampwidth(mic.chunk_size)
                #wf.setframerate(RATE)
                #wf.writeframes(b''.join(utteredFrames))
                #wf.close()

                return

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
                    hotwordCallback(mic);

    except KeyboardInterrupt:
        pass

    pixel_ring.off()


if __name__ == '__main__':
    main()
