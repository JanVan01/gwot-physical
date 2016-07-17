from controller.base import BaseController
from views.html import HtmlView
from models.config import ConfigManager
from models.locations import Locations
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
		sensor_id = None
		if sensor_data is not None and len(sensor_data) > 0:
			sensor_id = sensor_data[0].get_id()
		
		location = ConfigManager.Instance().get_location()
		locationObj = Locations().get(location)

		data = {
			"setup": False,
			"location": locationObj,
			"default_sensor": sensor_id,
			"sensors": {}
		}
		
		if locationObj is None or sensor_id is None:
			data["setup"] = True

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
				return str(value)
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
				return str(value)
			else:
				return self.unknownValue
			

	def config(self):
		return self.get_view('config.html').data()

	def config_password(self):
		return self.get_view('config_password.html').data()

	def config_sensors(self):
		return self.get_view('config_sensor.html').data()

	def config_notifications(self):
		return self.get_view('config_notifications.html').data()

	def config_locations(self):
		return self.get_view('config_location.html').data()

	def data(self):
		data = self.multi_model.get_all()
		model = self.get_model('models.locations', 'Locations')
		locations = model.get_all()

		model = self.get_model('models.sensors', 'Sensors')
		sensors = model.get_all()

		datacollection = {'measurements': data, 'locations': locations, 'sensors': sensors}
		return self.get_view('data.html').data(datacollection)

	def tutorial_sensors(self):
		return self.get_view('tutorial_sensors.html').data()

	def tutorial_notifications(self):
		return self.get_view('tutorial_notifications.html').data()
	
	def subscriptions(self):
		return self.get_view('subscriptions.html').data()

	def about(self):
		return self.get_view('about.html').data()
