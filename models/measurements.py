import psycopg2.extras
from models.base import BaseModel, BaseMultiModel

# Todo: Check whether python datetime and postgresqlsql datetime are transfered correctly
class Measurement(BaseModel):

	def __init__(self, db, id = None):
		super().__init__(db)
		self.id = id
		self.datetime = None
		self.value = None
		self.quality = None
		self.sensor = None
		self.location = None

	def from_dict(self, dict):
		self.set_id(dict['id'])
		self.set_datetime(dict['datetime'])
		self.set_value(dict['value'])
		self.set_quality(dict['quality'])
		self.set_sensor(dict['sensor'])
		self.set_location(dict['location'])

	def create(self):
		if self.sensor is None or self.location is None or self.value is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("INSERT INTO Measurements (value, quality, sensor, location) VALUES (%s, %s, %s, %s) RETURNING datetime, id", [self.value, self.quality, self.sensor, self.location])
		data = cur.fetchone()
		self.id = data['id']
		self.datetime = data['datetime']
		if self.id > 0:
			return True
		else:
			return False

	def read(self):
		if self.id is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("SELECT * FROM Measurements WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.from_dict(cur.fetchone())
			return True
		else:
			return False

	def update(self):
		if self.id is None or self.sensor is None or self.location is None or self.value is None:
			return False

		cur = self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
		cur.execute("UPDATE Measurements SET value = %s, quality = %s, sensor = %s, location = %s, datetime = %s WHERE id = %s", [self.value, self.quality, self.sensor, self.location, self.datetime, self.id])
		if cur.rowcount > 0:
			return True
		else:
			return False

	def delete(self):
		if self.id is None:
			return False

		cur = self.db.cursor()
		cur.execute("DELETE FROM Measurements WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.id = None
			return True
		else:
			return False

	def get_id(self):
		return self.id

	def set_id(self, id):
		self.id = id

	def get_datetime(self):
		return self.datetime

	def set_datetime(self, datetime):
		self.datetime = datetime

	def get_value(self):
		return self.value

	def set_value(self, value):
		self.value = value

	def get_quality(self):
		return self.quality

	def set_quality(self, quality):
		self.quality = quality

	def get_sensor(self):
		return self.sensor

	def get_sensor_object(self):
		from models.sensors import Sensors
		return Sensors(self.db).get(self.sensor)

	def set_sensor(self, sensor):
		from models.sensors import Sensor
		if isinstance(sensor, Sensor):
			self.sensor = sensor.get_id()
		else:
			self.sensor = sensor

	def get_location(self):
		return self.location

	def get_location_object(self):
		from models.locations import Locations
		return Locations(self.db).get(self.location)

	def set_location(self, location):
		from models.locations import Location
		if isinstance(location, Location):
			self.location = location.get_id()
		else:
			self.location = location


class Measurements(BaseMultiModel):

	def __init__(self, db):
		super().__init__(db)

	def create(self, pk = None):
		return Measurement(self.db, pk)

	def get_all(self):
		return self._get_all("SELECT * FROM Measurements ORDER BY id")

	def get_all_filtered(self, filter = None):
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_all("SELECT * FROM Measurements " + filterSql + " ORDER BY id")

	def get_last(self, filter = None):
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_one("SELECT * FROM Measurements " + filterSql + " ORDER BY id DESC LIMIT 1")

	def get_min(self, filter = None):
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_one("SELECT * FROM Measurements " + filterSql + " ORDER BY value ASC LIMIT 1")

	def get_max(self, filter = None):
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_one("SELECT * FROM Measurements " + filterSql + " ORDER BY value DESC LIMIT 1")

	def filter_defaults(self, args = None):
		defaults = {
			'outliers': None,
			'start': None,
			'end': None,
			'location': [],
			'coordinates': None,
			'sensor': []
		}
		if args is not None:
			defaults.update(args)
		return defaults


	def __build_filter(self, args, prefix):
		args = self.filter_defaults(args)
		conditions = []
		commaSeparator = ","

		if args['outliers'] != None and args['outliers'] == 1:
			conditions.append("quality > 0.5") # ToDo: What is a good quality?

# ToDo
#		if args['start'] != None:
#			conditions.append("datetime >= " + args['start'])


#		if args['end'] != None:
#			conditions.append("datetime <= " + args['end'])

		if len(args['location']) > 0:
			conditions.append("location IN(" + commaSeparator.join(args['location']) + ")");

		if len(args['sensor']) > 0:
			conditions.append("sensor IN(" + commaSeparator.join(args['sensor']) + ")");

#		if args['coordinates'] != None:
#			conditions.append("location = " + args['coordinates'])

		if len(conditions) > 0:
			op = " AND "
			return prefix + " " + op.join(conditions)
		else:
			return ""
