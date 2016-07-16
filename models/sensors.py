from utils.utils import Database, OS
from models.base import BaseModel, BaseMultiModel
from models.measurements import Measurements
from models.locations import Locations
from models.config import ConfigManager
from models.notifiers import Notifiers
from sensors.base import BaseSensor

class Sensor(BaseModel):
	
	def __init__(self, id = None):
		super().__init__(['id', 'module', 'class_name', 'type', 'description', 'unit', 'active', 'settings'])
		self.id = id
		self.module = None
		self.class_name = None
		self.type = None
		self.description = None
		self.unit = None
		self.active = False
		self.settings = None

	def from_dict(self, dict):
		super().from_dict(dict)
		if 'id' in dict:
			self.set_id(dict['id'])
		if 'module' in dict:
			self.set_module(dict['module'])
		if 'class' in dict:
			self.set_class(dict['class'])
		if 'type' in dict:
			self.set_type(dict['type'])
		if 'description' in dict:
			self.set_description(dict['description'])
		if 'unit' in dict:
			self.set_unit(dict['unit'])
		if 'active' in dict and dict['active'] is not None:
			self.set_active(dict['active'])
		if 'settings' in dict:
			self.set_settings(dict['settings'])

	def create(self):
		impl = self.get_sensor_impl()
		if impl is None or self.active is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("INSERT INTO Sensors (module, class, type, description, unit, active, settings) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", [self.module, self.class_name, impl.get_type(), self.description, impl.get_unit(), self.active, self._settings_dump(self.settings)])
		data = cur.fetchone()
		self.id = data['id']
		if self.id > 0:
			return True
		else:
			return False
	
	def read(self):
		if self.id is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("SELECT * FROM Sensors WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.from_dict(cur.fetchone())
			return True
		else:
			return False
	
	def update(self):
		impl = self.get_sensor_impl()
		if self.id is None or impl is None or self.active is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("UPDATE Sensors SET module = %s, class = %s, type = %s, description = %s, unit = %s, active = %s, settings = %s WHERE id = %s", [self.module, self.class_name, impl.get_type(), self.description, impl.get_unit(), self.active, self._settings_dump(self.settings), self.id])
		if cur.rowcount > 0:
			return True
		else:
			return False
	
	def delete(self):
		if self.id is None:
			return False

		cur = Database.Instance().cursor()
		cur.execute("DELETE FROM Sensors WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.id = None
			return True
		else:
			return False
		
	def get_id(self):
		return self.id
	
	def set_id(self, id):
		self.id = id
		
	def get_sensor_impl(self):
		obj = OS().create_object(self.module, self.class_name)
		if obj is not None:
			obj.set_settings(self.get_settings())
		return obj

	def set_sensor_impl(self, obj):
		if isinstance(obj, BaseSensor):
			self.module = obj.get_module()
			self.class_name = obj.get_class()

	def set_module(self, module):
		self.module = module
		
	def get_module(self):
		return self.module
		
	def get_class(self):
		return self.class_name
	
	def set_class(self, class_name):
		self.class_name = class_name
		
	def get_type(self):
		return self.type
	
	def set_type(self, type):
		self.type = type
		
	def get_description(self):
		return self.description
	
	def set_description(self, description):
		self.description = description
		
	def get_unit(self):
		return self.unit
	
	def set_unit(self, unit):
		self.unit = unit
		
	def is_active(self):
		return self.active
	
	def set_active(self, active):
		if self.active is None:
			return
		self.active = active
		
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
	
	
class Sensors(BaseMultiModel):
	
	def create(self, pk = None):
		return Sensor(pk)
	
	def get_all(self):
		return self._get_all("SELECT * FROM Sensors ORDER BY id")
	
	def get_pending(self):
		return self._get_all("SELECT s.*, EXTRACT(EPOCH FROM (NOW() - MAX(m.datetime)))/60 AS pending FROM Sensors s LEFT OUTER JOIN Measurements m ON m.sensor = s.id WHERE s.active = TRUE GROUP BY s.id")

	def get_by_class(self, module, class_name):
		return self._get_one("SELECT * FROM Sensors WHERE module = %s AND class = %s LIMIT 1", [module, class_name])
		
	def trigger_pending(self):
		interval = ConfigManager.Instance().get_interval()
		if interval < 1:
			return [] # No valid interval specified

		sensors = self.get_pending()
		return self.__trigger(sensors, True)
		
	
	def trigger_all(self):
		return self.__trigger(self.get_all())
	
	def __trigger(self, sensors, pending = False):
		data = []

		interval = None
		if pending is True:
			interval = ConfigManager.Instance().get_interval()
			if interval < 1:
				return [] # No valid interval specified
		
		location = Locations().get(ConfigManager.Instance().get_location())
		if location is None:
			return data; # No location found for this id

		measurements = Measurements()
		for sensor in sensors:
			# Sensor is disabled, ignore it
			if not sensor.is_active():
				continue
			
			# Ignore the sensor if no implementation can be found
			impl = sensor.get_sensor_impl()
			if impl is None:
				continue
				
			# If we want to trigger only pending sensors, check that and ignore sensors that are not pending to their rules
			if pending is True and impl.is_due(sensor.get_extra('pending'), interval) is False:
				continue

			measurementObj = None
			try:
				measurementObj = impl.get_measurement()
			except:
				print("Could not take a measurement for sensor " + str(sensor.get_id()))
			if measurementObj is not None:
				measurement = measurements.create()
				measurement.set_value(measurementObj.get_value())
				measurement.set_quality(measurementObj.get_quality())
				measurement.set_sensor(sensor)
				measurement.set_location(location)
				measurement.create()
				data.append(measurement)
				Notifiers().notify(measurement)

		return data