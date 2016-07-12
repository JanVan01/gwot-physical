from notifiers.base import BaseNotifier
import requests
import re

class OpenSenseMapNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		sensebox_id = notifier.get_setting("sensebox_id")
		sensor_id = subscriber.get_setting("sensor_id")
		if sensebox_id is None or sensor_id is None:
			print("OpenSenseMap notification not sent, sensebox_id or sensor_id not given.")
			return

		data = {"value": measurement.get_value()}
		url = "http://www.opensensemap.org:8000/boxes/" + sensebox_id + "/" + sensor_id
		headers = {"Content-type": "application/json", "Connection": "close"}

		r = requests.post(url, headers=headers, json=data)

		if r.status_code != 201:
			print("Sending OpenSenseMap notification to " + url + " and got response " + str(r.status_code))
	
	def get_subscriber_settings(self):
		return {"sensor_id"}
	
	def get_notifier_settings(self):
		return {"sensebox_id"}
	
	def get_setting_name(self, key):
		if key == "sensor_id":
			return "Sensor ID"
		elif key == "sensebox_id":
			return "Sensebox ID"
		else:
			return None
	
	def validate_setting(self, key, value):
		if key == "sensor_id" or key == "sensebox_id":
			regexp = "^[\dabcdef]{16,32}$"
			return (re.match(regexp, value) is not None)
		else:
			return False
	
	def get_setting_html(self, key):
		if key == "sensor_id" or key == "sensebox_id":
			return self._get_input_field(key, value)
		else:
			return None