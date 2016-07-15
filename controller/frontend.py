from controller.base import BaseController
from views.html import HtmlView
from models.config import ConfigManager
from models.locations import Locations
from models.sensors import Sensors
import time

class FrontendController(BaseController):

	def __init__(self):
		super().__init__()
		self.multi_model = self.get_model('models.measurements', 'Measurements')

	def get_view(self, template_file=None):
		view = HtmlView()
		if template_file is not None:
			view.set_template(template_file)
		return view

	def home(self):
		model = self.get_model('models.sensors', 'Sensors')
		sensor_data = model.get_all()
		data = {}
		for sensor in sensor_data:
			data[sensor.id] = self.__get_sensor_overview(sensor.id)
		return self.get_view('index.html').data(data)


	def __get_sensor_overview(self, sensor):
		location = ConfigManager.Instance().get_location()
		locationObj = Locations().get(location)
		if locationObj is not None:
			lon = locationObj.get_longitude()
			lat = locationObj.get_latitude()
		else:
			lon = None
			lat = None

		sensorObj = Sensors().get(sensor)
		if sensorObj is not None:
			sensor_type = sensorObj.get_type()
		else:
			sensor_type = "Unknown"

		item_data = {
			"sensor_id": sensor,
			"sensor_type": sensor_type,
			"minHourly": self.__getminmaxvalue(time.strftime("%Y-%m-%dT%H:00:00Z"), location, sensor),
			"maxHourly": self.__getminmaxvalue(time.strftime("%Y-%m-%dT%H:00:00Z"), location, sensor, False),
			"minDaily": self.__getminmaxvalue(time.strftime("%Y-%m-%dT00:00:00Z"), location, sensor),
			"maxDaily": self.__getminmaxvalue(time.strftime("%Y-%m-%dT00:00:00Z"), location, sensor, False),
			"minMonthly": self.__getminmaxvalue(time.strftime("%Y-%m-01T00:00:00Z"), location, sensor),
			"maxMonthly": self.__getminmaxvalue(time.strftime("%Y-%m-01T00:00:00Z"), location, sensor, False),
			"minYearly": self.__getminmaxvalue(time.strftime("%Y-01-01T00:00:00Z"), location, sensor),
			"maxYearly": self.__getminmaxvalue(time.strftime("%Y-01-01T00:00:00Z"), location, sensor, False),
			"minAccum": self.__getminmaxvalue(time.strftime("2015-01-01T00:00:00Z"), location, sensor),
			"maxAccum": self.__getminmaxvalue(time.strftime("2015-01-01T00:00:00Z"), location, sensor, False),
			"last": self.__getlastvalue(location, sensor),
			"lon": lon,
			"lat": lat
		}
		return item_data

	def __getlastvalue(self, location, sensor):
		filterObj = {
			'location': [str(location)],
			'sensor': [str(sensor)],
			'limit': 1
		}
		mlist = self.multi_model.get_last(filterObj)
		if len(mlist) == 0:
			return "None"
		else:
			return str(mlist[0].get_value())


	def __getminmaxvalue(self, start, location, sensor, min = True):
		filterObj = {
			'start': start,
			'location': [str(location)],
			'sensor': [str(sensor)],
			'limit': 1
		}
		if min is True:
			mlist = self.multi_model.get_min(filterObj)
		else:
			mlist = self.multi_model.get_max(filterObj)
		if len(mlist) == 0:
			return "None"
		else:
			return str(mlist[0].get_value())

	def config(self):
		data = {}
		return self.get_view('config.html').data(data)

	def config_password(self):
		data = {}
		return self.get_view('config_password.html').data(data)

	def config_sensors(self):
		data = {}
		return self.get_view('config_sensors.html').data(data)

	def config_locations(self):
		data = {}
		return self.get_view('config_locations.html').data(data)

	def data(self):
		data = self.multi_model.get_all()
		return self.get_view('data.html').data(data)

	def about(self):
		data = {}
		return self.get_view('about.html').data(data)
