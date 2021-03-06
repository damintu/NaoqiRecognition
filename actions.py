#!/usr/bin/env python

from naoqi import ALProxy
import env
import time


def walk_to_position(x, y, theta=0.0, freq=0.0):
    try:
        motion_proxy = ALProxy("ALMotion", env.nao_ip, env.nao_port)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
    else:
        motion_proxy.moveToward(x, y, theta, [["Frequency", freq]])


def do_action(string):
    rowing = False
    postureProxy = None
    tts = ALProxy("ALTextToSpeech", env.nao_ip, env.nao_port)
    try:
        postureProxy = ALProxy("ALRobotPosture", env.nao_ip, env.nao_port)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e
    if 'how are you' in '{}'.format(string):
        tts.say("I'm fine, how are you ?")
    elif 'thank you' in '{}'.format(string):
        tts.say("You're welcome !")
        add_positive()
    elif 'stand' in '{}'.format(string) and postureProxy is not None:
        postureProxy.goToPosture("Stand", 1.0)

    elif 'sit' in '{}'.format(string) and postureProxy is not None:
        postureProxy.goToPosture("Sit", 1.0)

    elif 'face' in '{}'.format(string):
        print "test1"
        tts = ALProxy("ALFaceDetection", env.nao_ip, env.nao_port)
        tts.enableTracking(True)
        tts.learnFace("damien")
        ALProxy("ALPhotoCaptureProxy", env.nao_ip, env.nao_port).takePicture()
        print "test"
    elif 'record' in '{}'.format(string) or 'recall' in '{}'.format(string):
        print "yolo bitch!"
        audioProxy = ALProxy("ALAudioRecorder", env.nao_ip, env.nao_port)
        audioProxy.startMicrophonesRecording("/home/nao/test.wav", "wav", 16000)
        time.sleep(15)
        audioProxy.stopMicrophonesRecording()
        print "done bitch!"

    elif 'moonwalk' in '{}'.format(string):
        if postureProxy.getPosture() != "Stand":
            postureProxy.goToPosture("Stand", 1.0)

        walk_to_position(-1.0, 0.0, 0.0, 1)

    elif 'walk' in '{}'.format(string):
        if postureProxy.getPosture() != "Stand":
            postureProxy.goToPosture("Stand", 1.0)
        walk_to_position(0.2, 0.3)
    elif 'row' in '{}'.format(string):
        if env.global_rowing == False:
            env.global_rowing = True
            rowing = True
        else:
            volume = tts.getVolume()
            tts.setVolume(1)
            tts.say("Fight the Power")
            tts.setVolume(volume)



    if not rowing:
        env.global_rowing = False

    # else:
    #     from pygoogle import pygoogle
    #     g = pygoogle('{}'.format(string))
    #     g.pages = 1
    #     print '*Found %s results*' % (g.get_result_count())
    #     import pdb; pdb.set_trace()
    #     g.get_urls()


def add_positive():
    env.nao_state_positive += 0.01
    if env.nao_state_positive > 1:
        env.nao_state_positive = 1
    print env.nao_state_positive
