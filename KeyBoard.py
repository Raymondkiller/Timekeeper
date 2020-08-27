#!/usr/bin/python
# -*- coding: utf8 -*-
########################################################################
#IdCardReader setup
########################################################################
import json
from evdev import InputDevice, categorize, ecodes
import os.path
from os import path

import threading
from MqttClient import MQTTClient

Mqtt = MQTTClient()
Mqtt.MqttPathPublish = "your path to publish"
Mqtt.MqttPathSubcribe = "KeyBoard"


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        Mqtt.mqttSubcribe()

# queueLock = threading.Lock()
# thread = myThread(1, "thread1")
# thread.start()

#########################################################################
flag_1 = False
_dataWriteMainApp = {"source":"KeyBoard","func":"capture","data":""}
_dataWriteAudioPlay = {"source":"KeyBoard","func":"play","data":""}
_dataWriteGPIO = {"source":"KeyBoard","func":"blinkLed","data":""}
_dataWriteAPIGetPost = {"source":"KeyBoard","func":"blinkLed","data":""}

print "start KeyBoard!"

#IdCardReader setup
while True:
    if path.exists('/dev/input/event0'):
        dev = InputDevice('/dev/input/event0')
        break
    else:
        _dataWriteAudioPlay["data"] = u"vui lòng kết nối máy quẹt thẻ trước"
        _dataWriteGPIO["data"] = "10"
        Mqtt.MqttPathPublish = "AudioPlay"
        Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))
        Mqtt.MqttPathPublish = "GPIO"
        Mqtt.mqttPublish(json.dumps(_dataWriteGPIO))

def readIDCardEvent():
    idCard = ""
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            #print "event",event
            if event.value == 0:
                if (event.code >= 2) & (event.code <= 10):
                    idCard = idCard + str(event.code - 1)
                #print "event.code",event.code
                if event.code == 11:
                    idCard = idCard + str(0)
                if event.code == 28:
                    break
    return idCard

while True:
    IDCardNumber = readIDCardEvent()
    print IDCardNumber
    #_dataWriteAPIGetPost["data"] = IDCardNumber
    _dataWriteMainApp["data"] = IDCardNumber
    Mqtt.MqttPathPublish = "MainApp"
    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
    #Mqtt.MqttPathPublish = "APIGetPost"
    #Mqtt.mqttPublish(json.dumps(_dataWriteAPIGetPost))
