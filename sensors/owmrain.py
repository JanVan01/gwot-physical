import pyowm
from sensors.base import BaseSensor, SensorMeasurement
from models.locations import Locations
from models.config import ConfigManager
from utils.utils import SettingManager

class OwmRainSnow(BaseSensor):
	
	def __init__(self):
		self.settings = None
		self.owm = None
		
	def get_type(self):
		return "OpenWeatherMap Rain+Snow"
	
	def get_unit(self):
		return "mm/3h"
	
	def get_measurement(self):
		if self.owm is None:
			api_key = self.get_setting("apikey")
			if api_key is None or len(api_key) < 1:
				return None
			self.owm = pyowm.OWM(api_key)
		
		lid = ConfigManager.Instance().get_location()
		if lid is None:
			return None

		location = Locations().get(lid)
		if location is None or location.get_latitude() is None or location.get_longitude() is None:
			return None

		obs = self.owm.weather_at_coords(location.get_latitude(), location.get_longitude()) 
		w = obs.get_weather()
		vol_rain = w.get_rain()
		vol_snow = w.get_snow()
		
		value = None
		quality = 1.0
		if '3h' in vol_rain and '3h' in vol_snow:
			value = vol_rain['3h'] + vol_snow['3h']
		elif '3h' in vol_rain:
			value = vol_rain['3h']
			quality = 0.5
		elif '3h' in vol_snow:
			value = vol_snow['3h']
			quality = 0.5
		else: # Not sure whether this is true (API returns nothing when there is no rain/snow?)
			value = 0
			quality = 0.0

		if value is not None:
			return SensorMeasurement(value, quality)
		else:
			return None
	
	def is_due(self, minutes, interval):
		return super().is_due(minutes, 60) # Free plan updates every 1 to 2 hours

	def get_setting_keys(self):
		return {"apikey"}
	
	def get_setting_name(self, key):
		if key == "apikey":
			return "OpenWeatherMap API Key"
		else:
			return None
	
	def validate_setting(self, key, value):
		if key == "apikey":
			return True
		else:
			return False
	
	def get_setting_html(self, key, value):
		if key == "apikey":
			return SettingManager().get_input_field(key, value)
		else:
			return None