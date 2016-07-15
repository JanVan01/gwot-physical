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
		self.unknownValue = "None"

	def get_view(self, template_file=None):
		view = HtmlView()
		if template_file is not None:
			view.set_template(template_file)
		return view

	def home(self):
		model = self.get_model('models.sensors', 'Sensors')
		sensor_data = model.get_all()
		
		location = ConfigManager.Instance().get_location()
		locationObj = Locations().get(location)
		if locationObj is not None:
			lon = locationObj.get_longitude()
			lat = locationObj.get_latitude()
			
		data = {
			"location": locationObj,
			"default_sensor": sensor_data[0].get_id(),
			"sensors": {}
		}

		for sensor in sensor_data:
			sensor_id = sensor.get_id()
			data['sensors'][sensor_id] = {
				"sensor": sensor,
				"hourly": self.__getminmaxavgvalue(time.strftime("%Y-%m-%dT%H:00:00Z"), location, sensor_id),
				"daily": self.__getminmaxavgvalue(time.strftime("%Y-%m-%dT00:00:00Z"), location, sensor_id),
				"monthly": self.__getminmaxavgvalue(time.strftime("%Y-%m-01T00:00:00Z"), location, sensor_id),
				"yearly": self.__getminmaxavgvalue(time.strftime("%Y-01-01T00:00:00Z"), location, sensor_id),
				"accum": self.__getminmaxavgvalue(time.strftime("2015-01-01T00:00:00Z"), location, sensor_id),
				"last": self.__getlastvalue(location, sensor_id)
			}

		return self.get_view('index.html').data(data)

	def __getlastvalue(self, location, sensor):
		filterObj = {
			'location': [str(location)],
			'sensor': [str(sensor)],
			'limit': 1
		}
		mlist = self.multi_model.get_last(filterObj)
		if len(mlist) == 0:
			return self.unknownValue
		else:
			value = mlist[0].get_value()
			if value is not None:
				return str(round(value, 1))
			else:
				return self.unknownValue

	def __getminmaxavgvalue(self, start, location, sensor):
		return {
			'min': self.__getaggregatevalue(start, location, sensor, 'min'),
			'avg': self.__getaggregatevalue(start, location, sensor, 'avg'),
			'max': self.__getaggregatevalue(start, location, sensor, 'max')
		}

	def __getaggregatevalue(self, start, location, sensor, type = 'avg'):
		filterObj = {
			'start': start,
			'location': [str(location)],
			'sensor': [str(sensor)],
			'limit': 1
		}
		if type == 'min':
			mlist = self.multi_model.get_min(filterObj)
		elif type == 'max':
			mlist = self.multi_model.get_max(filterObj)
		else:
			avg_obj = self.multi_model.get_avg(filterObj)
			mlist = [avg_obj]
		if len(mlist) == 0:
			return self.unknownValue
		else:
			value = mlist[0].get_value()
			if value is not None:
				return str(round(value, 1))
			else:
				return self.unknownValue
			

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
		model = self.get_model('models.locations', 'Locations')
		locations = model.get_all()

		model = self.get_model('models.sensors', 'Sensors')
		sensors = model.get_all()

		datacollection = {'measurements': data, 'locations': locations, 'sensors': sensors}
		return self.get_view('data.html').data(datacollection)

	def about(self):
		data = {}
		return self.get_view('about.html').data(data)
