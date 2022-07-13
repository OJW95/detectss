import RPi.GPIO as GPIO
import time

def detection(pinTrig, pinEcho):		
	GPIO.setup(pinTrig, GPIO.OUT)
	GPIO.setup(pinEcho, GPIO.IN)
	GPIO.output(pinTrig, True)
	time.sleep(0.00001)
	GPIO.output(pinTrig, False)

	while GPIO.input(pinEcho) == 0:
		start = time.time()
	while GPIO.input(pinEcho) == 1:
		stop = time.time()

	check_time = stop - start
	distance = check_time * 34300 / 2
	if distance > 30 and distance < 50:
		print("Distance : %.2f cm" % distance)
		return distance
	else:
		return False
