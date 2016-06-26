import psycopg2.extras
from models.base import BaseModel, BaseMultiModel
from models.measurements import Measurements
from models.locations import Location
from models.config import ConfigManager
from sensors.base import BaseSensor

class Sensor(BaseModel):
	
	def __init__(self, db, id = None):
		super().__init__(db, ['id', 'module', 'class_name', 'type', 'description', 'unit', 'active'])
		self.id = id
		self.module = None
		self.class_name = None
		self.type = None
		self.description = None
		self.unit = None
		self.active = False

	def from_dict(self, dict):
		self.set_id(dict['id'])
		self.set_module(dict['module'])
		self.set_class(dict['class'])
		self.set_type(dict['type'])
		self.set_description(dict['description'])
		self.set_unit(dict['unit'])
		if dict['active'] is not None:
			self.set_active(dict['active'])

	def create(self):
		impl = self.get_sensor_impl()
		if impl is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("INSERT INTO Sensors (module, class, type, description, unit, active) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", [self.module, self.class_name, impl.get_type(), self.description, impl.get_unit(), self.active])
		data = cur.fetchone()
		self.id = data['id']
		if self.id > 0:
			return True
		else:
			return False
	
	def read(self):
		if self.id is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("SELECT * FROM Sensors WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.from_dict(cur.fetchone())
			return True
		else:
			return False
	
	def update(self):
		impl = self.get_sensor_impl()
		if self.id is None or impl is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("UPDATE Sensors SET module = %s, class = %s, type = %s, description = %s, unit = %s, active = %s WHERE id = %s", [self.module, self.class_name, impl.get_type(), self.description, impl.get_unit(), self.active, self.id])
		if cur.rowcount > 0:
			return True
		else:
			return False
	
	def delete(self):
		if self.id is None:
			return False

		cur = self.db.cursor()
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
		return BaseSensor().create_object(self.module, self.class_name)

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
	
	
class Sensors(BaseMultiModel):

	def __init__(self, db):
		super().__init__(db)
	
	def create(self, pk = None):
		return Sensor(self.db, pk)
	
	def get_all(self):
		return self._get_all("SELECT * FROM Sensors ORDER BY id")
	
	def trigger_all(self):
		data = []

		config = ConfigManager()
		location = Location(self.db, config.get_location());
		if location.read() is False:
			return data; # No location found for this id

		measurements = Measurements(self.db)
		for sensor in self.get_all():
			# Sensor is disabled, ignore it
			if not sensor.is_active():
				continue
			
			# Ignore the sensor if no implementation can be found
			impl = sensor.get_sensor_impl()
			if impl is None:
				continue
	
			# ToDo: Check whether each sensotr should run or not (time-based)
			value = impl.get_measurement()
			if value is not None:
				measurement = measurements.create()
				measurement.set_value(value)
				measurement.set_quality(impl.get_quality())
				measurement.set_sensor(sensor)
				measurement.set_location(location)
				measurement.create()
				data.append(measurement)

		return data