########################################################################
#GPIO setup
########################################################################
import json
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

import threading
from MqttClient import MQTTClient

Mqtt = MQTTClient()
Mqtt.MqttPathPublish = "your path to publish"
Mqtt.MqttPathSubcribe = "GPIO"


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

_dataWriteMainApp = {"source":"GPIO","func":"interrupt","data":""}
_dataWriteAudioPlay = {"source":"GPIO","func":"play","data":""}

########################################################################
#GPIO setup
# LedWifi = 18
LedStatus = 15
interrupt1 = 22
interrupt2 = 22
interrupt3 = 22
interrupt4 = 22

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# #wifi status:
# GPIO.setup(LedWifi, GPIO.OUT, initial=GPIO.LOW) 
#trigger status: 
GPIO.setup(LedStatus, GPIO.OUT, initial=GPIO.LOW) 
#interrup:
GPIO.setup(interrupt1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(interrupt2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(interrupt3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(interrupt4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def interrupt_handler(channel):
    print("start interrupt trigger handler!")
    if channel == interrupt1:
        _dataWriteMainApp["data"] = "interrupt1"
    if channel == interrupt2:
        _dataWriteMainApp["data"] = "interrupt2"
    if channel == interrupt3:
        _dataWriteMainApp["data"] = "interrupt3"
    if channel == interrupt4:
        _dataWriteMainApp["data"] = "interrupt4"
    Mqtt.MqttPathPublish = "MainApp"
    Mqtt.mqttPublish(json.dumps(_dataWriteMainApp))
    print("stop interrupt trigger handler!")

GPIO.add_event_detect(interrupt1, GPIO.RISING, callback=interrupt_handler, bouncetime=200)
GPIO.add_event_detect(interrupt2, GPIO.RISING, callback=interrupt_handler, bouncetime=200)
GPIO.add_event_detect(interrupt3, GPIO.RISING, callback=interrupt_handler, bouncetime=200)
GPIO.add_event_detect(interrupt4, GPIO.RISING, callback=interrupt_handler, bouncetime=200)

def blinkLed(_number,_time,_timeDelay):
    for _t in range(_time):
        GPIO.output(_number, GPIO.HIGH) # Turn on
        time.sleep(_timeDelay)
        GPIO.output(_number, GPIO.LOW) # Turn off
        time.sleep(_timeDelay)

########################################################################

print "start GPIO!"
while True:
    _waitData = Mqtt.getData()
    if _waitData != None:
        waitData = json.loads(_waitData)
        blinkLed(LedStatus,waitData["data"],0.2)
