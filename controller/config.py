from controller.base import BaseController
from flask import request
from models.config import ConfigManager

class ConfigController(BaseController):

	def __init__(self):
		super().__init__()
		self.config = ConfigManager.Instance()

	def complete_config(self):
		if (request.method == 'GET'):
			data = {}
			data['name'] = self.config.get_name()
			data['interval'] = self.config.get_interval()
			print(data)
			return self.get_view(template_file='config.html').data(data)

	def location(self):
		return

	def password(self):
		if (request.method == 'GET'):
			data = self.config.get_password()
			return self.get_view().data(data)
		return self.get_view().error()

	def sensor(self):
		return

	def check_password(self, username):
		if username == "admin":
			return self.config.get_password()
		return None
