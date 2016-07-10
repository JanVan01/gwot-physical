from notifiers.base import BaseNotifier

class EmailNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		if measurement.get_quality() < 0.1:
			return # ignore measurements with a bad quality
		
		self._single(notifier, subscriber, measurement)
		self._byThreshold(notifier, subscriber, measurement)

	def _single(self, notifier, subscriber, measurement):
		print("Sending email notification to " + subscriber.get_connector() + " with value " + str(measurement.get_value()))
	
	def _byThreshold(self, notifier, subscriber, measurement):
		return