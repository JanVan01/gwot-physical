from utils.utils import Database
from models.base import BaseModel, BaseMultiModel

class Subscriber(BaseModel):

	def __init__(self, id = None):
		super().__init__(['id', 'notifier', 'sensor', 'settings'])
		self.id = id
		self.notifier = None
		self.sensor = None
		self.settings = None

	def from_dict(self, dict):
		super().from_dict(dict)
		if 'id' in dict:
			self.set_id(dict['id'])
		if 'notifier' in dict:
			self.set_notifier(dict['notifier'])
		if 'sensor' in dict:
			self.set_sensor(dict['sensor'])
		if 'settings' in dict:
			self.set_settings(dict['settings'])

	def create(self):
		if self.sensor is None or self.notifier is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("INSERT INTO Subscribers (settings, sensor, notifier) VALUES (%s, %s, %s, %s) RETURNING id", [self._settings_dump(self.settings), self.sensor, self.notifier])
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
		cur.execute("SELECT * FROM Subscribers WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.from_dict(cur.fetchone())
			return True
		else:
			return False

	def update(self):
		if self.id is None or self.sensor is None or self.notifier is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("UPDATE Subscribers SET settings = %s, sensor = %s, notifier = %s WHERE id = %s", [self._settings_dump(self.settings), self.sensor, self.notifier, self.id])
		if cur.rowcount > 0:
			return True
		else:
			return False

	def delete(self):
		if self.id is None:
			return False

		cur = Database.Instance().cursor()
		cur.execute("DELETE FROM Subscribers WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.id = None
			return True
		else:
			return False

	def get_id(self):
		return self.id

	def set_id(self, id):
		self.id = id
		
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

	def get_notifier(self):
		return self.notifier

	def get_notifier_object(self):
		from models.notifiers import Notifiers
		return Notifiers().get(self.notifier)

	def set_notifier(self, notifier):
		from models.notifiers import Notifier
		if isinstance(notifier, Notifier):
			self.notifier = notifier.get_id()
		else:
			self.notifier = notifier


class Subscribers(BaseMultiModel):

	def create(self, pk = None):
		return Subscriber(pk)

	def get_all(self):
		return self._get_all("SELECT * FROM Subscribers ORDER BY id")

	def get_all_active_by_sensor(self, sensor_id):
		return self._get_all("SELECT s.* FROM Subscribers s INNER JOIN Notifiers n ON s.notifier = n.id WHERE n.active = true And s.sensor = %s", [sensor_id])
