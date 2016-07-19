from utils.utils import Database, OS, ThreadObserver
from models.base import BaseModel, BaseMultiModel
from notifiers.base import BaseNotifier
from models.subscribers import Subscribers
import threading

class Notifier(BaseModel):

	def __init__(self, id = None):
		super().__init__(['id', 'module', 'class_name', 'name', 'description', 'settings', 'public', 'active'])
		self.id = id
		self.module = None
		self.class_name = None
		self.name = None
		self.description = None
		self.settings = None
		self.active = False
		self.public = False

	def from_dict(self, dict):
		super().from_dict(dict)
		if 'id' in dict:
			self.set_id(dict['id'])
		if 'module' in dict:
			self.set_module(dict['module'])
		if 'class' in dict:
			self.set_class(dict['class'])
		if 'name' in dict:
			self.set_name(dict['name'])
		if 'description' in dict:
			self.set_description(dict['description'])
		if 'settings' in dict:
			self.set_settings(dict['settings'])
		if 'public' in dict and dict['public'] is not None:
			self.set_public(dict['public'])
		if 'active' in dict and dict['active'] is not None:
			self.set_active(dict['active'])

	def create(self):
		impl = self.get_notifier_impl()
		if impl is None or self.active is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("INSERT INTO Notifiers (module, class, name, description, settings, public, active) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id", [self.module, self.class_name, self.name, self.description, self._settings_dump(self.settings), self.public, self.active])
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
		cur.execute("SELECT * FROM Notifiers WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.from_dict(cur.fetchone())
			return True
		else:
			return False

	def update(self):
		impl = self.get_notifier_impl()
		if self.id is None or impl is None or self.active is None:
			return False

		cur = Database.Instance().dict_cursor()
		cur.execute("UPDATE Notifiers SET module = %s, class = %s, name = %s, description = %s, settings = %s, public = %s, active = %s WHERE id = %s", [self.module, self.class_name, self.name, self.description, self._settings_dump(self.settings), self.public, self.active, self.id])
		if cur.rowcount > 0:
			return True
		else:
			return False

	def delete(self):
		if self.id is None:
			return False

		cur = Database.Instance().cursor()
		cur.execute("DELETE FROM Notifiers WHERE id = %s", [self.id])
		if cur.rowcount > 0:
			self.id = None
			return True
		else:
			return False

	def get_id(self):
		return self.id

	def set_id(self, id):
		self.id = id

	def get_notifier_impl(self):
		obj = OS().create_object(self.module, self.class_name)
		if obj is not None:
			obj.set_settings(self.get_settings())
		return obj

	def set_notifier_impl(self, obj):
		if isinstance(obj, BaseNotifier):
			self.module = obj.get_module()
			self.class_name = obj.get_class()

	def set_module(self, module):
		self.module = module

	def get_module(self):
		return self.module

	def get_class(self):
		return self.class_name

	def get_classpath(self):
		return self.module + '.' + self.class_name

	def set_class(self, class_name):
		self.class_name = class_name

	def get_name(self):
		return self.name

	def set_name(self, name):
		self.name = name

	def get_description(self):
		return self.description

	def set_description(self, description):
		self.description = description

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

	def is_active(self):
		return self.active

	def set_active(self, active):
		if self.active is None:
			return
		self.active = active

	def is_public(self):
		return self.public

	def set_public(self, public):
		if not self.get_notifier_impl().is_public():
			return;
		if self.public is None:
			return
		self.public = public

class Notifiers(BaseMultiModel):

	def create(self, pk = None):
		return Notifier(pk)

	def get_all(self):
		return self._get_all("SELECT * FROM Notifiers ORDER BY id")

	def get_all_active_public(self):
		return self._get_all("SELECT * FROM Notifiers WHERE public = TRUE AND active = TRUE ORDER BY name")

	def notify(self, measurement):
		thread = NotificationThread(measurement)
		thread.daemon = True
		thread.start()


class NotificationThread(threading.Thread):

	def __init__(self, measurement):
		super().__init__()
		self.measurement = measurement
		ThreadObserver.Instance().add(self)

	def run(self):
		# Get all relevant subscribtions
		subs = Subscribers().get_all_active_by_sensor(self.measurement.get_sensor())

		if len(subs) > 0:
			# Cache all notifiers + implementations in a list with ids as keys
			notifiers = {}
			for entry in Notifiers().get_all():
				impl = entry.get_notifier_impl()
				impl.prepare()
				notifiers[entry.get_id()] = {
					"model": entry,
					"impl": impl
				}

			# Go thorugh all subscribers and send notification
			for sub in subs:
				notifier = notifiers[sub.get_notifier()]
				try:
					notifier.impl.send(notifier.model, sub, self.measurement)
				except:
					print("Could not send notification of type " + notifier.impl.get_module() + "." + notifier.impl.get_class())

		ThreadObserver.Instance().remove(self)
