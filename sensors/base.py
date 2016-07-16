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
		if isinstance(settings, str):
			settings = self._settings_load(settings)
		self.settings = settings
		
class SensorMeasurement(object):
	def __init__(self, value, quality = None):
		self.value = value
		self.quality = quality
		
	def get_value(self):
		return self.value
	
	def get_quality(self):
		return self.quality