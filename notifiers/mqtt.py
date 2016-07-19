from notifiers.base import BaseNotifier
# needed to push messages to MQTT
import paho.mqtt.publish as publish
from utils.utils import SettingManager
import re

# Takes some input (data) and pushs it to the MQTT-broker 'mosquitto'.
# Subscrubers of the channel 'everyMeasurement' will recieve all measurements

class MqttNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		value = measurement.get_value()
		threshold = subscriber.get_setting('threshold')
		if value > threshold:
			topic = subscriber.get_setting('topic')
			publish.single(topic, str(value), hostname="localhost")

		#self._publish_every_measurement(notifier, subscriber, measurement)
		#self._publish_by_threshold(notifier, subscriber, measurement)

	def _publish_every_measurement(self, notifier, subscriber, measurement):
		message = str(measurement.get_value()).encode('unicode_escape')
		publish.single("everyMeasurement", message, hostname="localhost")

	def _publish_by_threshold(self, notifier, subscriber, measurement):
		value = measurement.get_value()
		if value > 200:
			message = str(value).encode('unicode_escape')
			publish.single("publishByThreshold", message, hostname="localhost")

	def get_subscriber_settings(self):
		return ['topic', 'threshold']

	def get_setting_name(self, key):
		if key == 'topic':
			return 'Topic on the MQTT-broker'
		elif key == 'threshold':
			return 'Threshold which has to be exeeded to trigger a notification'
		else:
			return None

	def validate_setting(self, key, value):
		if key == "threshold":
			regexp = '^[-+]?\d+\.?\d*$'
			return (re.match(regexp, value) is not None)
		elif key == 'topic':
			return True
		else:
			return False

	def get_setting_html(self, key, value=None):
		if key == 'topic' or key == 'threshold':
			return SettingManager().get_input_field(key, value)
		else:
			return None
