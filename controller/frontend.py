from controller.base import BaseController
from views.html import HtmlView
from models.config import ConfigManager
from models.locations import Locations
from models.sensors import Sensors
from flask import request
import time

class FrontendController(BaseController):

	def __init__(self):
		super().__init__()
		self.multi_model = self.get_model('models.measurements', 'Measurements')
		self.config_manager = ConfigManager.Instance()
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
		data['name'] = self.config_manager.get_name()
		data['interval'] = self.config_manager.get_interval()
		data['location'] = self._get_location(self.config_manager.get_location())
		data['sensors'] = self._get_sensors()
		if 'mode' in request.args and request.args['mode'] == 'edit':
			data['all_locations'] = self._get_all_locations()
			return self.get_view('config_edit.html').data(data)
		return self.get_view('config.html').data(data)

	def config_password(self):
		return self.get_view('config_password.html').data({})

	def config_sensors(self):
		data = {}
		if 'mode' in request.args and request.args['mode'] == 'edit' and 'id' in request.args:
			sensor = self.get_model('models.sensors', 'Sensors').get(request.args['id'])
			if sensor is not None:
				data['mode'] = 'edit'
				data['id'] = sensor.get_id()
				data['module'] = sensor.get_module()
				data['class_name'] = sensor.get_class()
				data['type'] = sensor.get_type()
				data['description'] = sensor.get_description()
				data['unit'] = sensor.get_unit()
				return self.get_view('config_sensor.html').data(data)
		return self.get_view('config_sensor.html').data(data)

	def config_locations(self):
		data = {}
		if 'mode' in request.args and request.args['mode'] == 'edit' and 'id' in request.args:
			location = self.get_model('models.locations', 'Locations').get(request.args['id'])
			if location is not None:
				data['mode'] = 'edit'
				data['id'] = location.get_id()
				data['name'] = location.get_name()
				data['lat'] = location.get_latitude()
				data['lon'] = location.get_longitude()
				data['height'] = location.get_height()
				return self.get_view('config_location.html').data(data)
		return self.get_view('config_location.html').data(data)

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

	def _get_location(self, id):
		location_model = self.get_model('models.locations', 'Location')
		location_model.set_id(id)
		location_model.read()
		location = {}
		location['id'] = location_model.get_id()
		location['name'] = location_model.get_name()
		location['lat'] = location_model.get_latitude()
		location['lon'] = location_model.get_longitude()
		location['height'] = location_model.get_height()
		return location

	def _get_all_locations(self):
		locations_model = self.get_model('models.locations', 'Locations')
		locations = []
		for l in locations_model.get_all():
			location = {}
			location['id'] = l.get_id()
			location['name'] = l.get_name()
			location['lat'] = l.get_latitude()
			location['lon'] = l.get_longitude()
			location['height'] = l.get_height()
			locations.append(location)
		return locations

	def _get_sensors(self):
		sensor_model = self.get_model('models.sensors', 'Sensors')
		sensors = []
		for s in sensor_model.get_all():
			sensor = {}
			sensor['id'] = s.get_id()
			sensor['module'] = s.get_module()
			sensor['class_name'] = s.get_class()
			sensor['type'] = s.get_type()
			sensor['description'] = s.get_description()
			sensor['unit'] = s.get_unit()
			sensors.append(sensor)
		return sensors
