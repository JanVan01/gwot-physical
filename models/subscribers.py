from utils.utils import Database
from models.base import BaseModel, BaseMultiModel

class Subscriber(BaseModel):

	def __init__(self, id = None):
		super().__init__(['id', 'notifier', 'sensor', 'connector', 'settings'])
		self.id = id
		self.notifier = None
		self.sensor = None
		self.connector = None
		self.settings = None

	def from_dict(self, dict):
		self.set_id(dict['id'])
		self.set_notifier(dict['notifier'])
		self.set_sensor(dict['sensor'])
		self.set_connector(dict['connector'])
		self.set_settings(dict['settings'])

	def create(self):
		if self.sensor is None or self.notifier is None or self.connector is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("INSERT INTO Subscribers (connector, settings, sensor, notifier) VALUES (%s, %s, %s, %s) RETURNING id", [self.connector, self.settings, self.sensor, self.notifier])
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
		if self.id is None or self.sensor is None or self.notifier is None or self.connector is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("UPDATE Subscribers SET connector = %s, settings = %s, sensor = %s, notifier = %s WHERE id = %s", [self.connector, self.settings, self.sensor, self.notifier, self.id])
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

	def get_connector(self):
		return self.connector

	def set_connector(self, connector):
		self.connector = connector

	def get_settings(self):
		return self.settings

	def set_settings(self, settings):
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
