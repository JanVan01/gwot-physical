import smtplib
from email.mime.text import MIMEText
from notifiers.base import BaseNotifier
from models.config import ConfigManager

class EmailNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		if measurement.get_quality() < 0.1:
			return # ignore measurements with a bad quality
		
		self._single(notifier, subscriber, measurement)
		self._byThreshold(notifier, subscriber, measurement)

	def _single(self, notifier, subscriber, measurement):
		name = ConfigManager.Instance().get_name()
		fromAddr = "no-reply@mamo-net.de" # notifier.get_settings().fromAddr
		self._send_mail(
			"New measurement notification from " + name,
			"Device: " + name + "\r\nMeasurement value: " + str(measurement.get_value()) + "\r\nMeasurement quality: " + str(measurement.get_quality()),
			subscriber.get_connector(),
			fromAddr
		)
		print("Sending email notification to " + subscriber.get_connector() + " with value " + str(measurement.get_value()))
	
	def _byThreshold(self, notifier, subscriber, measurement):
		return
	
	def _send_mail(self, subject, message, toAddr, fromAddr):
		msg = MIMEText(message)
		msg['Subject'] = subject
		msg['To'] = toAddr # the recipient's email address
		msg['From'] = fromAddr # the sender's email address

		# Send the message via our own SMTP server, but don't include the envelope header.
		s = smtplib.SMTP('localhost')
		s.sendmail(fromAddr, [toAddr], msg.as_string())
		s.quit()