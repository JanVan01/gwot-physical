
from models.config import ConfigManager
from controller.base import BaseController

class ConfigController(BaseController):

	def __init__(self):
		super().__init__()
		self.config = ConfigManager()

	def name(self):
		return

	def height(self):
		return
		
	def location(self):
		return
		
	def interval(self):
		return
	
	def password(self):
		return
	
	def sensor(self):
		return
	
	def check_password(self, username):
		if username == "admin":
			return self.config.get_password()
		return None