import threading
from MqttClient import MQTTClient

Mqtt = MQTTClient()
Mqtt.MqttPathPublish = "killer"

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

print Mqtt.MqttServer,Mqtt.MqttPort
while True:
	t = Mqtt.getData()
	if t != None:
		print "client get: ", t
		Mqtt.mqttPublish("killer")

