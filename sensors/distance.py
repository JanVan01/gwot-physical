# Description:
# Signatur: tirgger_reading: -> number
# Purpose: Function triggers a distance-measurement and
#		  returns the calculated distance in [cm].
# Author:   Niklas Trzaska, Oleg Stepanov
#		   Code for function from
#		   http://www.bytecreation.com/blog/2013/10/13/raspberry-pi-ultrasonic-sensor-hc-sr04
#		   and modified according purpose.
import math
import RPi.GPIO as GPIO
from sensors.base import BaseSensor, SensorMeasurement
import time


class DistanceSensor(BaseSensor):
	
	def __init__(self):
		self.trigger_pin = 17
		self.data_pin = 27
		
		# Warnings disabled
		GPIO.setwarnings(False)

		GPIO.setmode(GPIO.BCM)

		# Define used GPIOs
		GPIO.setup(self.trigger_pin, GPIO.OUT)
		GPIO.setup(self.data_pin, GPIO.IN)
		GPIO.output(self.trigger_pin, GPIO.LOW)

		# Avoid crashs
		time.sleep(0.5)
		
		
	def get_type(self):
		return "HC-SR04"
	
	def get_unit(self):
		return "cm"
	
	def get_measurement(self):
		raw_data = []

		# We try 20 times and leave 10 attempts for invalid measurements
		for i in range(20):
			next_call = time.time() + 0.5

			# Send signal
			GPIO.output(self.trigger_pin, True)

			# Sensor expects a puls-length of 10Us
			time.sleep(0.00001)

			# Stop pulse
			GPIO.output(self.trigger_pin, False)
			
			signalon = None
			signaloff = None

			# listen to the input pin.
			# 0:= no input
			# 1:= input measured
			begin_time = time.time()
			while GPIO.input(self.data_pin) == 0:
				signaloff = time.time()
				if (signaloff - begin_time) > 2: # Don't run into endless loops
					signaloff = None
					break
					
			if signaloff is None:
				continue

			while GPIO.input(self.data_pin) == 1:
				signalon = time.time()
				if (signalon - begin_time) > 2: # Don't run into endless loops
					signalon = None
					break
			
			# If there is no valid measurement result return
			if signalon is None:
				continue

			# calculate distance
			timepassed = signalon - signaloff

			# convert distance into cm
			raw_distance = timepassed * 17000
			if raw_distance > 3000:
				continue
			else:
				# append data to the list
				raw_data.append(raw_distance)

				# wait for the time left between measurments
				time.sleep(next_call-time.time())
				
				# If wen have enough measurements, break loop
				if len(raw_data) >= 10:
					break
		
		# If there is not enough data, skip
		if len(raw_data) < 8:
			return None

		# sort the measurements
		sorted(raw_data)
		# delete 2 minimum and 2 max measurements
		trimmed_data = raw_data[2:-2]
		trimmed_data_length = len(trimmed_data)
		#calculate mean value
		value = sum(trimmed_data)/(trimmed_data_length)
		
		#calculate standard deviation
		sd = math.sqrt(sum([(item-value)**2 for item in trimmed_data])/trimmed_data_length)
		if sd > 5:
			quality = 0.0
		else:
			quality = 1.0
		return SensorMeasurement(value, quality)