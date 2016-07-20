from notifiers.base import BaseNotifier
# needed to push messages to MQTT
import paho.mqtt.publish as publish
import re
from utils.utils import SettingManager

# Takes some input (data) and pushs it to the MQTT-broker 'mosquitto'.
# Subscrubers of the channel 'everyMeasurement' will recieve all measurements


class MqttNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		value = measurement.get_value()
		threshold = subscriber.get_setting('threshold')
		topic = subscriber.get_setting('topic')
		if threshold == '':
			publish.single(topic, str(value), hostname="localhost")
		elif value > float(threshold):
			publish.single(topic, str(value), hostname="localhost")

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
			if value == '':
				return True
			regexp = '^[-+]?\d+\.?\d*$'
			return (re.match(regexp, value) is not None)
		elif key == 'topic' and value != '':
			return True
		else:
			return False

	def get_setting_html(self, key, value=None):
		if key == 'topic' or key == 'threshold':
			return SettingManager().get_input_field(key, value)
		else:
			return None

	def is_public(self):
		return False
