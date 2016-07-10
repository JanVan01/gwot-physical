import smtplib
import re
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
		fromAddr = notifier.get_setting("sender")
		self._send_mail(
			"New measurement notification from " + name,
			"Device: " + name + "\r\nMeasurement value: " + str(measurement.get_value()) + "\r\nMeasurement quality: " + str(measurement.get_quality()),
			subscriber.get_setting('email'),
			fromAddr
		)
	
	def _byThreshold(self, notifier, subscriber, measurement):
		return
	
	def is_public(self):
		return True
	
	def _send_mail(self, subject, message, toAddr, fromAddr):
		msg = MIMEText(message)
		msg['Subject'] = subject
		msg['To'] = toAddr # the recipient's email address
		msg['From'] = fromAddr # the sender's email address

		# Send the message via our own SMTP server, but don't include the envelope header.
		s = smtplib.SMTP('localhost')
		s.sendmail(fromAddr, [toAddr], msg.as_string())
		s.quit()

	def get_subscriber_settings(self):
		return {"email"}
	
	def get_notifier_settings(self):
		return {"sender"}

	def get_setting_name(self, key):
		if key == "email":
			return "E-mail address to be notified"
		elif key == "sender":
			return "Sending e-mail address"
		else:
			return None
	
	def validate_setting(self, key, value):
		if key == "email" or key == "sender":
			regexp = "^[^@]+@[^@]+\.[^@]+$"
			return (re.match(regexp, value) is not None)
		else:
			return False
	
	def get_setting_html(self, key, value):
		if key == "email" or key == "sender":
			return self._get_input_field(key, value)
		else:
			return None