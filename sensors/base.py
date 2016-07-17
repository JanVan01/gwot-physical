from utils.utils import Transform

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
	
	def low_precision(self):
		return 0
	
	def high_precision(self):
		return 2
	
	def is_due(self, minutes, interval):
		return (minutes is None or minutes >= interval)
	
	def get_setting_keys(self):
		return {}
	
	def get_setting_name(self, key):
		return None
	
	def validate_setting(self, key, value):
		return False
	
	def get_setting_html(self, key, value):
		return None
		
	def get_setting(self, key):
		if self.settings is not None and key in self.settings:
			return self.settings[key]
		else:
			return None

	def get_settings(self):
		if self.settings is None:
			return {}
		else:
			return self.settings

	def set_settings(self, settings):
		self.settings = settings
		
	def _round(self, value):
		return Transform().round(value, self.high_precision())
		
class SensorMeasurement(object):
	def __init__(self, value, quality = None):
		self.value = value
		self.quality = quality
		
	def get_value(self):
		return self.value
	
	def get_quality(self):
		return round(self.quality, 2)