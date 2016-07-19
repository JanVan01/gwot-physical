import smtplib
import re
from email.mime.text import MIMEText
from notifiers.base import BaseNotifier
from models.config import ConfigManager
from models.measurements import Measurements
from models.sensors import Sensors
from utils.utils import SettingManager

class EmailNotifier(BaseNotifier):

	def send(self, notifier, subscriber, measurement):
		if measurement.get_quality() < 0.1:
			return # ignore measurements with a bad quality
		
		name = ConfigManager.Instance().get_name()
		fromAddr = notifier.get_setting("sender")
		self._send_mail(
			"New measurement notification from " + name,
			"Device: " + name + "\r\nMeasurement value: " + str(measurement.get_value()) + "\r\nMeasurement quality: " + str(measurement.get_quality()),
			subscriber.get_setting('email'),
			fromAddr
		)
	
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
		return ["email"]
	
	def get_notifier_settings(self):
		return ["sender"]

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
	
	def get_setting_html(self, key, value = None):
		if key == "email" or key == "sender":
			return SettingManager().get_input_field(key, value)
		else:
			return None
		

class EmailTrendNotifier(EmailNotifier):
	
	def __init__(self):
		self.trend_data = {}
		self.hour_limit = 24

	def prepare(self):
		location = ConfigManager.Instance().get_location()
		sensors = Sensors().get_all()
		for sensor in sensors:
			self.trend_data[sensor.get_id()] = Measurements().calc_trend(sensor.get_id(), location)

	def send(self, notifier, subscriber, measurement):
		if measurement.get_sensor() not in self.trend_data:
			return
		
		limit = self.get_setting("limit")
		critical = Measurements().reaches_limit_in_time(limit, self.hour_limit, self.trend_data[measurement.get_sensor()])
		if critical is False:
			return
		
		name = ConfigManager.Instance().get_name()
		fromAddr = self.get_setting("sender")
		self._send_mail(
			"New measurement notification from " + name,
			"Device: " + name + "\r\nMeasurement value: " + str(measurement.get_value()) + "\r\nMeasurement quality: " + str(measurement.get_quality()),
			subscriber.get_setting('email'),
			fromAddr
		)

	def get_subscriber_settings(self):
		parent = super().get_subscriber_settings()
		parent.append("limit")
		return parent

	def get_setting_name(self, key):
		if key == "limit":
			return "Boundary which needs to be reached in 24 hours to be notified"
		else:
			return super().get_setting_name(key)
	
	def validate_setting(self, key, value):
		if key == "limit":
			return Validate().floating(value)
		else:
			return super().validate_setting(key, value)
	
	def get_setting_html(self, key, value = None):
		if key == "limit":
			return SettingManager().get_input_field(key, value, "float")
		else:
			return super().get_setting_html(key, value)