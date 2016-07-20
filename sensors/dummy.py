from sensors.base import BaseSensor, SensorMeasurement
import random

class DummySensor(BaseSensor):
		
	def get_type(self):
		return "Dummy Random"
	
	def get_unit(self):
		return "dummy"
	
	def get_measurement(self):
		value = random.randint(1, 1000)
		value = self.round(value)
		return SensorMeasurement(value, random.random())