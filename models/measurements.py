from utils.utils import Database
from models.base import BaseModel, BaseMultiModel

# Todo: Check whether python datetime and postgresqlsql datetime are transfered correctly
class Measurement(BaseModel):

	def __init__(self, id = None):
		super().__init__(['id', 'datetime', 'value', 'quality', 'sensor', 'location'])
		self.id = id
		self.datetime = None
		self.value = None
		self.quality = None
		self.sensor = None
		self.location = None

	def from_dict(self, dict):
		if 'id' in dict:
			self.set_id(dict['id'])
		if 'datetime' in dict:
			self.set_datetime(dict['datetime'])
		if 'value' in dict:
			self.set_value(dict['value'])
		if 'quality' in dict:
			self.set_quality(dict['quality'])
		if 'sensor' in dict:
			self.set_sensor(dict['sensor'])
		if 'location' in dict:
			self.set_location(dict['location'])

	def create(self):
		if self.sensor is None or self.location is None or self.value is None:
			return False

		cur = Database.Instance().dict_cursor()
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

		cur = Database.Instance().dict_cursor()
		cur.execute("SELECT * FROM Measurements WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.from_dict(cur.fetchone())
			return True
		else:
			return False

	def update(self):
		if self.id is None or self.sensor is None or self.location is None or self.value is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("UPDATE Measurements SET value = %s, quality = %s, sensor = %s, location = %s, datetime = %s WHERE id = %s", [self.value, self.quality, self.sensor, self.location, self.datetime, self.id])
		if cur.rowcount > 0:
			return True
		else:
			return False

	def delete(self):
		if self.id is None:
			return False

		cur = Database.Instance().cursor()
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
		return Sensors().get(self.sensor)

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
		return Locations().get(self.location)

	def set_location(self, location):
		from models.locations import Location
		if isinstance(location, Location):
			self.location = location.get_id()
		else:
			self.location = location


class Measurements(BaseMultiModel):

	def create(self, pk = None):
		return Measurement(pk)

	def get_all(self, filter = None):
		filter = self.filter_defaults(filter)
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_all("SELECT m.* FROM Measurements m " + filterSql + " ORDER BY m.id ASC LIMIT " + str(filter['limit']))

	def get_last(self, filter = None):
		filter = self.filter_defaults(filter, 1)
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_all("SELECT m.* FROM Measurements m " + filterSql + " ORDER BY m.id DESC LIMIT " + str(filter['limit']))

	def get_min(self, filter = None):
		filter = self.filter_defaults(filter, 1)
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_all("SELECT m.* FROM Measurements m " + filterSql + " ORDER BY m.value ASC LIMIT " + str(filter['limit']))

	def get_avg(self, filter = None):
		filter = self.filter_defaults(filter, 1)
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_one("SELECT AVG(m.value) AS value FROM Measurements m " + filterSql + " LIMIT 1")

	def get_max(self, filter = None):
		filter = self.filter_defaults(filter, 1)
		filterSql = self.__build_filter(filter, "WHERE")
		return self._get_all("SELECT m.* FROM Measurements m " + filterSql + " ORDER BY m.value DESC LIMIT " + str(filter['limit']))

	def filter_defaults(self, args = None, limit = 100):
		defaults = {
			'start': None,
			'end': None,
			'location': [],
			'geometry': None,
			'sensor': [],
			'limit': limit
		}
		if args is not None:
			defaults.update(args)
		return defaults


	def __build_filter(self, args, prefix):
		args = self.filter_defaults(args)
		conditions = []
		commaSeparator = ","

		if args['start'] is not None:
			conditions.append("m.datetime >= timestamp '" + args['start'] + "'")

		if args['end'] is not None:
			conditions.append("m.datetime <= timestamp '" + args['end'] + "'")

		if len(args['location']) > 0:
			conditions.append("m.location IN(" + commaSeparator.join(args['location']) + ")");

		if len(args['sensor']) > 0:
			conditions.append("m.sensor IN(" + commaSeparator.join(args['sensor']) + ")");

		if args['geometry'] is not None:
			prefix = " INNER JOIN Locations l ON m.location = l.id " + prefix
			conditions.append("ST_Intersects(l.geom, ST_GeographyFromText('" + args['geometry'] + "'))")

		if len(conditions) > 0:
			op = " AND "
			return prefix + " " + op.join(conditions)
		else:
			return ""
