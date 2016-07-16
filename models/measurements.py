from utils.utils import Database
from models.base import BaseModel, BaseMultiModel
from models.config import ConfigManager

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
		super().from_dict(dict)
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
	
	def calc_trend(self, sensor, location = None):
		if location is None:
			location = ConfigManager.Instance().get_location()
		
		last = self.get_last({
			"sensor": [sensor],
			"location": [location],
			"limit": 1000,
			"quality": 0.25
		})
		
		data = {
			"since": None,
			"until": None,
			"change_abs": 0,
			"change_perhour": 0
		}
		
		if len(last) < 3:
			return data # Not enough data for calculation
		
		# Calculate whether its ascending or descending
		direction = 0
		old = last[0].get_value()
		older = last[1].get_value()
		oldest = last[2].get_value()
		if oldest > older and older > old and old != oldest:
			direction = -1 # descending
		if oldest <= older and older <= old and old != oldest:
			direction = 1 # ascending

		if direction == 0:
			return data # No trend
		
		# Find how long the trend is
		outliers = 0
		pivot = 0
		prev_is_outlier = False
		i = 0
		# Iterate over all elements until we have two outliers in a row, elements are getting older with increasing index
		while i < len(last)-1 and outliers < 2:
			i += 1
			this = last[i-1].get_value()
			prev = last[i].get_value()
			
			# Check whether values are equal or are getting smaller/larger
			if (direction == 1 and prev <= this) or (direction == -1 and prev >= this):
				# If the elemts are equal...
				if (prev == this):
					 # check if the previous entry was an outlier and if this one is the same value, end loop as we reached two outliers
					if prev_is_outlier is True:
						break
				# Value is smaller or larger
				else:
					pivot = i
					# If previous element was not an outlier, we can decrease the number of outliers
					if prev_is_outlier is False:
						outliers -= 1
			# We detected an outlier
			else:
				outliers += 1
				prev_is_outlier = True
		
		newest = last[0]
		oldest = last[pivot]

		data['since'] = oldest.get_datetime()
		data['until'] = newest.get_datetime()
		data['change_abs'] = abs(newest.get_value() - oldest.get_value()) * direction
		
		timedelta = data['until'] - data['since']
		hourdelta = timedelta.total_seconds() / (60*60)
		data['change_perhour'] = hourdelta / data['change_abs']

		return data

	def filter_defaults(self, args = None, limit = 100):
		defaults = {
			'start': None,
			'end': None,
			'location': [],
			'geometry': None,
			'quality': None,
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

		if not isinstance(args['location'], list):
			args['location'] = [args['location']]
		if len(args['location']) > 0:
			conditions.append("m.location IN(" + commaSeparator.join(str(x) for x in args['location']) + ")");

		if not isinstance(args['sensor'], list):
			args['sensor'] = [args['sensor']]
		if len(args['sensor']) > 0:
			conditions.append("m.sensor IN(" + commaSeparator.join(str(x) for x in args['sensor']) + ")");

		if args['geometry'] is not None:
			prefix = " INNER JOIN Locations l ON m.location = l.id " + prefix
			conditions.append("ST_Intersects(l.geom, ST_GeographyFromText('" + args['geometry'] + "'))")

		if args['quality'] is not None:
			conditions.append("m.quality >= " + str(args['quality']))

		if len(conditions) > 0:
			op = " AND "
			return prefix + " " + op.join(conditions)
		else:
			return ""
