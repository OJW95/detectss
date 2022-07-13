import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from utils import Utils
from dht11 import collect, filter_extract
from hcsr04 import detection
import cv2

MQTT_ERR_SUCCESS = 0

pinDht = 18
pinTrig = 6
pinEcho = 5
utils = Utils()
camera = cv2.VideoCapture(0)
client = mqtt.Client('Detector')

def init():
	GPIO.setmode(GPIO.BCM)
	# MQTT_INIT
	client.connect('54.157.12.31')
	print("""
			IR_DETECTOR_ON
MQTT_COMUNICATION_ON
""".strip())

try:
	init()
	while True:

		if(detection(pinTrig, pinEcho)):
			print('detect')
			img_num = utils.capture(camera)
			if img_num == -1:
				print('Capture Fail')
			else:
				url = utils.post(img_num)
				if url is False:
	 				print('Upload Fail')
				else:
					#qos '1' fixed NOMATCH error! why?
					r, _ = client.publish('image', url, 0)
					if r == MQTT_ERR_SUCCESS:
						print('Pulished')
						if utils.close(camera):
							camera = cv2.VideoCapture(-1)
					else:
						print('Publish Fail')
		data = collect(pinDht)
		humid, humidf, temper, temperf, crc = filter_extract(data)
		if (humid + humidf + temper + temperf) == crc:
			humid = str(humid) + '.' + str(humidf) + '%'
			temper = str(temper) + '.' + str(temperf) + '*C'
			r, _ = client.publish('humid', humid)
			if r == MQTT_ERR_SUCCESS:
			   print('Published humid')
			r, _ = client.publish('temper', temper)
			if r == MQTT_ERR_SUCCESS:
			   print('Published temper')
		time.sleep(3)

except KeyboardInterrupt:
	utils.close(camera)
	GPIO.cleanup()
	print("DETECTION STOP")
