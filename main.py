import sys
import logging
import AWSIoTPythonSDK
import json
import time
import random
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

Lat  = 33.748995
Long = -84.387982
def seedGPS(seed):
	random.seed(seed)
	Lat = random.uniform(-90, 90)
	Long = random.uniform(-180, 180)

def moveGps():
	global Lat, Long
	tmp = random.uniform(-.1, .1)
	if not abs(tmp + Lat) > 90:
		Lat = Lat + tmp
	tmp = random.uniform(-.1, .1)
	if not abs(tmp + Long) > 180:
		Long = Long + tmp

# seedGPS(7)
# while True:
# 	moveGps()
# 	print "Lat: %s  Long %s ", Lat, Long

def subCallBack(client, userdata, message):
	tmp = json.loads(message.payload)
	print(client)
	print("Received a new message: ")
	print(tmp)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

''' Set up logging for simple debugging '''
logger = logging.getLogger('AWSIoTPythonSDK.core')
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

''' Setup connection '''
MQTTClient = AWSIoTMQTTClient("myClientID")
MQTTClient.configureCredentials("./cert/rootCA.pem", "./cert/private.key", "./cert/cert.pem")
MQTTClient.configureEndpoint("a6i7sqcw5o0o.iot.us-east-1.amazonaws.com", 8883)

MQTTClient.configureOfflinePublishQueueing(-1)
MQTTClient.configureDrainingFrequency(2)
MQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
MQTTClient.configureMQTTOperationTimeout(5)




MQTTClient.connect()
# myMQTTClient.publish("myTopic", "myPayload", 0)
# MQTTClient.subscribe("my/out", 1, subCallBack)
# MQTTClient.unsubscribe("myTopic")
# MQTTClient.disconnect()

while True:
	moveGps()
	tmp = json.dumps({"latitude": Lat, "longitude": Long})
	MQTTClient.publish("Device/GPS", tmp, 0)
	time.sleep(3)
	pass


if __name__ == '__main__':
	main()