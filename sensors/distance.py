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
from models.locations import Locations
from models.config import ConfigManager
from models.measurements import Measurements
from models.sensors import Sensors
from utils.utils import SettingManager
from utils.utils import Validate
import time


class DistanceSensor(BaseSensor):

	def __init__(self):
		self.settings = None
		self.prepared = False

	def __prepare(self):
		if self.prepared is True:
			return self.prepared

		self.trigger_pin = self.get_setting("trigger_pin")
		self.data_pin = self.get_setting("data_pin")
		if self.trigger_pin is None or self.data_pin is None:
			print('Please configure pins of distance sensor.')
			return False

		self.prepared = True
		self.trigger_pin = int(self.trigger_pin)
		self.data_pin = int(self.data_pin)

		# Warnings disabled
		GPIO.setwarnings(False)

		GPIO.setmode(GPIO.BCM)

		# Define used GPIOs
		GPIO.setup(self.trigger_pin, GPIO.OUT)
		GPIO.setup(self.data_pin, GPIO.IN)
		GPIO.output(self.trigger_pin, GPIO.LOW)

		# Avoid crashs
		time.sleep(0.5)
		return self.prepared


	def get_type(self):
		return "HC-SR04"

	def get_unit(self):
		return "cm"

	def get_measurement(self):
		if not self.__prepare():
			return None;

		raw_data = []

		# We try 20 times and leave 10 attempts for invalid measurements
		for i in range(20):
			if i > 5 and len(raw_data) == 0:
				return None # Sensor seems not to be configured corretly, skip execution

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
		raw_data.sort()
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
		value = self.round(value)
		return SensorMeasurement(value, quality)

	def high_precision(self):
		return 1

	def is_due(self, minutes, interval):
		if minutes is None: # No measurement so far
			return True

		weatherSensor = Sensors().get_by_class('sensors.owmrain', 'OwmRainSnow')
		if weatherSensor is not None:
			weatherMeasurements = Measurements().get_last({
				"sensor": [weatherSensor.get_id()],
				"limit": 1,
				"location": [ConfigManager.Instance().get_location()]
			})

			new_interval = interval
			if len(weatherMeasurements) > 0:
				value = weatherMeasurements[0].get_value()
				if value > 30:
					new_interval = 2 # Measure every two minutes in case of heavy rain
				elif value > 0:
					new_interval = interval/2 # Double the speed in case of light rain

			if new_interval < interval:
				interval = new_interval

		return (minutes >= interval)

	def get_setting_keys(self):
		return ["trigger_pin", "data_pin"]

	def get_setting_name(self, key):
		if key == "trigger_pin":
			return "Trigger Pin on Pi"
		elif key == "data_pin":
			return "Data Pin on Pi"
		else:
			return None

	def validate_setting(self, key, value):
		if key == "trigger_pin" or key == "data_pin":
			return Validate().integer(value)
		else:
			return False

	def get_setting_html(self, key, value = None):
		if key == "trigger_pin" or key == "data_pin":
			return SettingManager().get_input_field(key, value, "number")
		else:
			return None

class GaugeSensor(DistanceSensor):

	def get_measurement(self):
		lid = ConfigManager.Instance().get_location()
		data = super().get_measurement()
		if lid is None or data is None:
			return None

		location = Locations().get(lid)
		if location is None or location.get_height() is None:
			return None

		value = location.get_height() - data.get_value()
		value = self.round(value)
		return SensorMeasurement(value, data.get_quality())
