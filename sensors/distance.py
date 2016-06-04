# Description:
# Signatur: tirgger_reading: -> number
# Purpose: Function triggers a distance-measurement and
#		  returns the calculated distance in [cm].
# Author:   Niklas Trzaska,
#		   Code for function from
#		   http://www.bytecreation.com/blog/2013/10/13/raspberry-pi-ultrasonic-sensor-hc-sr04
#		   and modified according purpose.

import RPi.GPIO as GPIO
from sensors.base import BaseSensor
import time

class DistanceSensor(BaseSensor):
	
	def __init__(self):
		# Warnings disabled
		GPIO.setwarnings(False)

		GPIO.setmode(GPIO.BCM)

		# Define used GPIOs
		GPIO.setup(17, GPIO.OUT)
		GPIO.setup(27, GPIO.IN)
		GPIO.output(17, GPIO.LOW)

		# Avoid crashs
		time.sleep(0.5)
		
		
	def get_type(self):
		return "HC-SR04"
	
	def get_unit(self):
		return "cm"
	
	def get_quality(self):
		return None # ToDo: Add quality flag
	
	def get_measurement(self):
		# Send signal
		GPIO.output(17, True)

		# Sensor expects a puls-length of 10Us
		time.sleep(0.00001)

		# Stop pulse
		GPIO.output(17, False)

		# listen to the input pin.
		# 0:= no input
		# 1:= input measured
		while GPIO.input(27) == 0:
			signaloff = time.time()

		while GPIO.input(27) == 1:
			signalon = time.time()

		# calculate distance
		timepassed = signalon - signaloff

		# convert distance into cm
		distance = timepassed * 17000

		return distance
