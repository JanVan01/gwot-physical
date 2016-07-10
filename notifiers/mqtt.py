import paho.mqtt.publish as publish # needed to push messages to subscribers
from notifiers.base import BaseNotifier

# Takes some input (data) and pushs it to the MQTT-broker 'mosquitto'.
# Subscrubers of the channel 'everyMeasurement' will recieve all measurements

class MqttNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		self._publish_every_measurement(notifier, subscriber, measurement)
		self._publish_by_threshold(notifier, subscriber, measurement)
	
	def _publish_every_measurement(self, notifier, subscriber, measurement):
		message = str(measurement.get_value()).encode('unicode_escape')
		publish.single("everyMeasurement", message, hostname="localhost")

	def _publish_by_threshold(self, notifier, subscriber, measurement):
		value = measurement.get_value();
		if value > 200:
			message = str(value).encode('unicode_escape')
			publish.single("publishByThreshold", message, hostname="localhost")