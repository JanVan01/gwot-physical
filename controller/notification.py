from controller.base import BaseController
from models.notifiers import Notifiers
from models.subscribers import Subscribers
from models.sensors import Sensors
from flask import request

class NotificationController(BaseController):
		
	def list(self):
		data = Notifiers().get_all_active_public()
		return self.get_view().data(data)

	def subscription(self):
		input = request.get_json()
		if input is None:
			return self.get_view().bad_request('Expected json')
		if 'notifier' in input and 'sensor' in input and 'settings' in input:
			notifier = Notifiers().get(input['notifier'])
			if notifier is None or not notifier.is_public():
				return self.get_view().bad_request('Not a valid notifier')
			sensor = Sensors().get(input['sensor'])
			if sensor is None:
				return self.get_view().bad_request('Not a valid sensor')

			subscription = Subscribers().create()
			try:
				subscription.set_notifier(int(input['notifier']))
				subscription.set_sensor(int(input['sensor']))
				# ToDo: Validate subscription settings
				subscription.set_settings(input['settings'])
				if not subscription.create():
					return self.get_view().bad_request('The subscription you are trying to create does not exist try to create it instead')
			except ValueError:
				return self.get_view().bad_request('input not in the right format')
		else:
			return self.get_view().bad_request('not all necessary field set')
		return self.get_view().success()
