#!/usr/bin/python
# -*- coding: utf-8 -*-
########################################################################
#audio setup
########################################################################
import json
import os.path
from os import path
import pygame
import os

from gtts import gTTS

import threading
from MqttClient import MQTTClient

Mqtt = MQTTClient()
Mqtt.MqttPathPublish = "your path to publish"
Mqtt.MqttPathSubcribe = "AudioPlay"


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        Mqtt.mqttSubcribe()

queueLock = threading.Lock()
thread = myThread(1, "thread1")
thread.start()

########################################################################
#audio setup
def playAudio(_filename):
    pygame.mixer.init()
    _file = "/home/pi/maychamcong/audio/" + _filename.encode('utf-8') + ".mp3"
    if not os.path.exists(_file):
        myobj = gTTS(text=unicode(_filename.encode('utf-8'), "utf-8"), lang='vi', slow=False)  
        myobj.save(_file)
    pygame.mixer.music.load(_file)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        pass

def playTextToAudio(_text, _language):
    myobj = gTTS(text=unicode(_text.encode('utf-8'), "utf-8"), lang=_language, slow=False)  
    myobj.save(_text + ".mp3")
########################################################################

print "start AudioPlay!"
while True:
    _waitData = Mqtt.getData()
    if _waitData != None:
	print _waitData
        waitData = json.loads(_waitData)
        playAudio(waitData["data"])
#	print waitData["data"].encode('utf-8')
#	print unicode(waitData["data"].encode('utf-8'), "utf-8")
