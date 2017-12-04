# sound.py
# Contains mapping of Dialogflow Intents to WAV files and sample rates and a play function that randomises sample rate slightly

import array
from random import randint
import os
import numpy as np
from pydub import AudioSegment

intent_map = {
        'hey_luko'                      : ['hey.wav', 4],
        'smalltalk.agent.acquaintance'  : ['acq.wav', 4],
        'smalltalk.agent.age'           : ['age.wav', 4],
        'smalltalk.agent.birth\_date'   : ['dob.wav', 4],
        'smalltalk.agent.busy'          : ['busy.wav', 4],
        'smalltalk.agent.can\_you\_help': ['help.wav', 3],
        'smalltalk.agent.chatbot'       : ['chatbot.wav', 5],
        'smalltalk.agent.hungry'        : ['hungry.wav', 6],
        'smalltalk.agent.marry\_user'   : ['marry.wav', 3],
        'smalltalk.agent.my\_friend'    : ['friend.wav', 3],
        'smalltalk.dialog.how\_are\_you': ['dhay.wav', 4],
        'smalltalk.agent.real'          : ['real.wav', 3],
        'smalltalk.agent.there'         : ['there.wav', 4],
        'smalltalk.appraisal.good'      : ['good.wav', 2],
        'smalltalk.appraisal.no\_problem': ['np.wav', 3],
        'smalltalk.appraisal.thank\_you': ['thx.wav', 3],
        'smalltalk.appraisal.well\_done': ['wd.wav', 2],
        'smalltalk.appraisal.welcome'   : ['welcome.wav', 3],
        'smalltalk.dialog.i\_do\_not\_care': ['idc.wav', 5],
        'smalltalk.dialog.sorry'        : ['sorry.wav', 3],
        'smalltalk.dialog.what\_do\_you\_mean': ['wdym.wav', 4],
        'smalltalk.dialog.wrong'        : ['wrong.wav', 5],
        'smalltalk.emotions.ha\_ha'     : ['haha.wav', 2],
        'smalltalk.emotions.wow'        : ['wow.wav', 3],
        'smalltalk.greetings.bye'       : ['bye.wav', 3],
        'smalltalk.greetings.goodevening': ['ge.wav', 4],
        'smalltalk.greetings.goodmorning': ['gm.wav', 4],
        'smalltalk.greetings.goodnight' : ['gn.wav', 3],
        'smalltalk.greetings.hello'     : ['hello.wav', 4],
        'smalltalk.greetings.how\_are\_you': ['ghay.wav', 4],
        'smalltalk.greetings.nice\_to\_meet\_you': ['ntmy.wav', 3],
        'smalltalk.greetings.nice\_to\_talk\_to\_you': ['nttty.wav', 3],
        'smalltalk.greetings.whatsup'   : ['whatsup.wav', 3],
        'smalltalk.user.bored'          : ['bored.wav', 5],
        'smalltalk.user.happy'          : ['happy.wav', 2],
        'smalltalk.user.sad'            : ['sad.wav', 6],
        'smalltalk.user.sleepy'         : ['sleepy.wav', 5],
        'smalltalk.user.testing\_agent' : ['test.wav', 2],
        'test_intent'                   : ['a.wav', 3],
        'default'                       : ['e.wav', 5]
    }


def play(intent):

    try:
        audio_file = intent_map[intent][0]
        rate = intent_map[intent][1] + (randint(-9,9)/10)
    except KeyError:
        audio_file = intent_map["default"][0]
        rate = intent_map["default"][1] + (randint(-9,9)/10)

    song = AudioSegment.from_wav("sounds/" + audio_file)

    samples = song.get_array_of_samples()

    sampled = np.delete(samples, np.arange(0, len(samples), rate))

    result = song._spawn(array.array(song.array_type, sampled))

    filename = "luko_sound_" + str(rate) + ".wav"

    result.export(filename, format="wav")

    # Play generated sound file and then delete the file
    os.system("aplay " + filename)
    os.remove(filename)
