from MqttClient import MQTTClient
import json

Mqtt = MQTTClient()

_dataWriteAudioPlay = {"source":"APIGetPost","func":"play","data":""}
_dataWriteAudioPlay["data"] = "truongtrinhdakhoidongxong"
Mqtt.MqttPathPublish = "AudioPlay"

Mqtt.mqttPublish(json.dumps(_dataWriteAudioPlay))
print "test"
