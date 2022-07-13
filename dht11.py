import RPi.GPIO as GPIO
import time

def collect(pin):
	data = []
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	time.sleep(0.025)
	GPIO.output(pin, GPIO.LOW)
	time.sleep(0.14)
	GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

	for i in range(0, 1500):
		data.append(GPIO.input(pin))
	return data

def filter_extract(data):
	seek = 0
	bits_max = 0
	bits_min = 9999
	effectiveData = []
	HumidityBit = ""
	HumidityBitD = ""
	TemperatureBit = ""
	TemperatureBitD = ""
	crcBit = ""

	while(seek < len(data) and data[seek] == 0):
		seek += 1
	while(seek < len(data) and data[seek] == 1):
		seek += 1

	for i in range(0, 40):
		bbuffer = ""

		while(seek < len(data) and data[seek] == 0):
			seek += 1

		while(seek < len(data) and data[seek] == 1):
			seek += 1
			bbuffer += "1"

		if(len(bbuffer) < bits_min):
			bits_min = len(bbuffer)

		if(len(bbuffer) > bits_max):
			bits_max = len(bbuffer)

		effectiveData.append(bbuffer)

	for i in range(0, len(effectiveData)):
		if (len(effectiveData[i]) < ((bits_max + bits_min)/2)):
			effectiveData[i] = "0"
		else:
	 		effectiveData[i] = "1"

	for i in range(0, 8):
		HumidityBit += str(effectiveData[i])

	for i in range(8, 16):
		HumidityBitD += str(effectiveData[i])

	for i in range(16, 24):
		TemperatureBit += str(effectiveData[i])

	for i in range(24, 32):
		TemperatureBitD += str(effectiveData[i])

	for i in range(32, 40):
		crcBit += str(effectiveData[i])

	return int(HumidityBit, 2), int(HumidityBitD, 2), int(TemperatureBit, 2), int(TemperatureBitD, 2), int(crcBit, 2)

#pin = 17

#while True:
#	data = collect()
#	humid, humidf, temper, temperf, crc = filter_extract(data)
#
#	if ((humid + temper + humidf + temperf) == crc):
#		print("Humidity = %d.%d %% Temperature = %d.%d *C"%(humid, humidf, temper, temperf))
