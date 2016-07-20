from controller.base import BaseController
from models.config import ConfigManager
from models.locations import Locations
from models.measurements import Measurements
from models.notifiers import Notifiers
from models.sensors import Sensors
from models.subscribers import Subscribers
from views.html import HtmlView
from utils.utils import OS
from flask import request
import time

class FrontendController(BaseController):

	def __init__(self):
		super().__init__()
		self.config_manager = ConfigManager.Instance()
		self.unknownValue = "None"

	def get_view(self, template_file=None):
		view = HtmlView()
		if template_file is not None:
			view.set_template(template_file)
		return view

	def home(self):
		sensor_data = Sensors().get_all()
		sensor_id = None
		if sensor_data is not None and len(sensor_data) > 0:
			sensor_id = sensor_data[0].get_id()

		location = ConfigManager.Instance().get_location()
		locationObj = Locations().get(location)

		data = {
			'setup': False,
			'location': locationObj,
			'default_sensor': sensor_id,
			'sensors': {}
		}

		if locationObj is None or sensor_id is None:
			data['setup'] = True

		for sensor in sensor_data:
			sensor_id = sensor.get_id()
			last = self.__getlastvalue(location, sensor_id)
			data['sensors'][sensor_id] = {
				'sensor': sensor,
				'hourly': self.__getminmaxavgvalue(time.strftime('%Y-%m-%dT%H:00:00Z'), location, sensor),
				'daily': self.__getminmaxavgvalue(time.strftime('%Y-%m-%dT00:00:00Z'), location, sensor),
				'monthly': self.__getminmaxavgvalue(time.strftime('%Y-%m-01T00:00:00Z'), location, sensor),
				'yearly': self.__getminmaxavgvalue(time.strftime('%Y-01-01T00:00:00Z'), location, sensor),
				'accum': self.__getminmaxavgvalue(time.strftime('2015-01-01T00:00:00Z'), location, sensor),
				'last': last['last'],
				'datetime': last['datetime'],
				'trend': Measurements().calc_trend(sensor_id, location)['description']
			}
		return self.get_view('index.html').data(data)

	def __getlastvalue(self, location, sensor):
		filterObj = {
			'location': [str(location)],
			'sensor': [str(sensor)],
			'limit': 1
		}
		mlist = Measurements().get_last(filterObj)
		
		if len(mlist) > 0:
			value = mlist[0].get_value()
			if value is not None:
				return {'last': str(value), 'datetime': mlist[0].datetime.strftime("%a %b %d %Y %H:%M:%S")}
		
		return {'last': self.unknownValue, 'datetime': self.unknownValue}

	def __getminmaxavgvalue(self, start, location, sensor):
		return {
			'min': self.__getaggregatevalue(start, location, sensor, 'min'),
			'avg': self.__getaggregatevalue(start, location, sensor, 'avg'),
			'max': self.__getaggregatevalue(start, location, sensor, 'max')
		}

	def __getaggregatevalue(self, start, location, sensor, type='avg'):
		filterObj = {
			'start': start,
			'location': [str(location)],
			'sensor': [str(sensor.get_id())],
			'limit': 1
		}
		multi_model = Measurements()
		if type == 'min':
			mlist = multi_model.get_min(filterObj)
		elif type == 'max':
			mlist = multi_model.get_max(filterObj)
		else:
			avg_obj = multi_model.get_avg(filterObj)
			mlist = [avg_obj]
		if len(mlist) == 0:
			return self.unknownValue
		else:
			value = mlist[0].get_value()
			if value is not None:
				impl = sensor.get_sensor_impl()
				if impl is not None:
					value = impl.round(value)
				return str(value)
			else:
				return self.unknownValue

	def _get_module_chooser(self, title, url, folder, suffix):
		data = {
			"title": title,
			"target": url,
			"modules": OS().get_classes(folder, suffix)
		}
		return self.get_view('config_module_chooser.html').data(data)

	def config(self):
		data = {
			"config": ConfigManager.Instance(),
			"locations": Locations().get_all()
		}
		return self.get_view('config.html').data(data)

	def config_password(self):
		return self.get_view('config_password.html').data()

	def config_sensors(self):
		data = {"sensors": Sensors().get_all()}
		return self.get_view('config_sensor.html').data(data)

	def config_sensors_change(self, mode, id):
		if mode == 'add' and 'module' not in request.args:
			if request.method == 'POST':
				filename = OS().upload_file('sensors/', 'file');
			return self._get_module_chooser("Add Sensor", "/config/sensors/add", "sensors", "Sensor")

		data = {
			"edit": (mode == 'edit'),
			"mode": mode,
			"sensor": None,
			"sensor_impl": None,
			"sensor_module": None,
			"modules": OS().get_classes("sensors", "Sensor")
		}
		if mode == 'edit' and id is not None:
			sensor = Sensors().get(id)
			data['sensor'] = sensor
			data['sensor_module'] = sensor.get_classpath()
			data['sensor_impl'] = sensor.get_sensor_impl()
		elif mode == 'add':
			data['sensor_module'] = request.args.get('module')
			data['sensor_impl'] = OS().create_object(data['sensor_module'])

		return self.get_view('config_sensor_change.html').data(data)

	def config_locations(self):
		data = {
			"locations": Locations().get_all(),
			"default_location": ConfigManager.Instance().get_location()
		}

		return self.get_view('config_location.html').data(data)

	def config_locations_change(self, mode, id):
		data = {
			"edit": (mode == 'edit'),
			"mode": mode,
			"location": None
		}
		if mode == 'edit' and id is not None:
			location = Locations().get(id)
			data['location'] = location

		return self.get_view('config_location_change.html').data(data)

	def config_notifications(self):
		data = {
			"notifiers": Notifiers().get_all()
		}
		return self.get_view('config_notifications.html').data(data)

	def config_notifications_change(self, mode, nid):
		if mode == 'add' and 'module' not in request.args:
			if request.method == 'POST':
				filename = OS().upload_file('notifiers/', 'file')
			return self._get_module_chooser("Add Notification Service", "/config/notifications/add", "notifiers", "Notifier")

		data = {
			"edit": (mode == 'edit'),
			"mode": mode,
			"notifier": None,
			"notifier_impl": None,
			"notifier_module": None,
			"modules": OS().get_classes("notifiers", "Notifier")
		}
		if mode == 'edit' and nid is not None:
			notifier = Notifiers().get(nid)
			data['notifier'] = notifier
			data['notifier_module'] = notifier.get_classpath()
			data['notifier_impl'] = notifier.get_notifier_impl()
		elif mode == 'add':
			data['notifier_module'] = request.args.get('module')
			data['notifier_impl'] = OS().create_object(data['notifier_module'])

		return self.get_view('config_notifications_change.html').data(data)

	def config_subscriptions(self, nid):
		notifier = Notifiers().get(nid)
		notifier_impl = notifier.get_notifier_impl()
		data = {
			"notifier": notifier,
			"notifier_impl": notifier_impl,
			"subscribers": Subscribers().get_all_by_notifier(nid)
		}
		return self.get_view('config_subscriptions.html').data(data)

	def config_subscriptions_change(self, mode, nid, sid):
		data = {
			"edit": (mode == 'edit'),
			"mode": mode,
			"subscriber": None,
			"notifier": None,
			"notifier_impl": None,
			"sensors": Sensors().get_all()
		}
		if mode == 'edit' and nid is not None:
			subscriber = Subscribers().get(sid)
			data['subscriber'] = subscriber
			data['notifier'] = subscriber.get_notifier_object()
		elif mode == 'add':
			data['notifier'] = Notifiers().get(nid)
		data["notifier_impl"] = data['notifier'].get_notifier_impl()

		return self.get_view('config_subscriptions_change.html').data(data)

	def data(self):
		data = {
			'locations': Locations().get_all(),
			'sensors': Sensors().get_all(),
			'timerange': Measurements().get_time_range()
		}
		return self.get_view('data.html').data(data)

	def tutorial_sensors(self):
		return self.get_view('tutorial_sensors.html').data()

	def tutorial_notifications(self):
		return self.get_view('tutorial_notifications.html').data()

	def subscriptions(self):
		data = Notifiers().get_all_active_public()
		return self.get_view('subscriptions.html').data(data)

	def subscriptions_add(self, id):
		notifier = Notifiers().get(id)
		data = {
			"notifier": notifier,
			"notifier_impl": notifier.get_notifier_impl(),
			"sensors": Sensors().get_all()
		}
		return self.get_view('subscriptions_add.html').data(data)

	def about(self):
		return self.get_view('about.html').data()
