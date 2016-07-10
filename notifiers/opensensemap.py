from notifiers.base import BaseNotifier
import requests

class OpenSenseMapNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		sensebox_id = "" # ToDo: Get from settings
		sensor_id = "" # ToDo: Get from settings

		data = {"value": measurement.get_value()}
		url = "http://www.opensensemap.org:8000/boxes/" + sensebox_id + "/" + sensor_id
		headers = {"Content-type": "application/json", "Connection": "close"}

		r = requests.post(url, headers=headers, json=data)

		print("Sending OpenSenseMap notification to " + subscriber.get_connector() + " with value " + str(measurement.get_value()) + " and got response " + str(r.status_code))