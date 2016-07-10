from notifiers.base import BaseNotifier

class OpenSenseMapNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		print("Sending OpenSenseMap notification to " + subscriber.get_connector() + " with value " + str(measurement.get_value()))