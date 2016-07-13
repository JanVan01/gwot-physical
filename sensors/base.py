class BaseSensor(object):
	
	def get_class(self):
		return self.__class__.__name__
		
	def get_module(self):
		return self.__module__
		
	def get_type(self):
		return None
	
	def get_unit(self):
		return None
	
	def get_measurement(self):
		return None
		
class SensorMeasurement(object):
	def __init__(self, value, quality = None):
		self.value = value
		self.quality = quality
		
	def get_value(self):
		return self.value
	
	def get_quality(self):
		return self.quality