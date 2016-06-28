import configparser
from utils.singleton import Singleton

@Singleton
class ConfigManager(object):

	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('data/config.ini')

	def save_config(self):
		with open('data/config.ini', 'w') as c:
			self.config.write(c)

	def reset_default(self):
		self.config['Config'] = self.config['Default']
		self.save_config()

	def get_name(self):
		return self.config['Config']['name']

	def set_name(self, name):
		self.config['Config']['name'] = name
		self.save_config()

	def get_location(self):
		return int(self.config['Config']['location'])

	def set_location(self, id):
		try:
			self.config['Config']['location'] = int(id)
			self.save_config()
		except ValueError:
			raise

	def get_interval(self):
		return int(self.config['Config']['interval'])

	def set_interval(self, interval):
		try:
			self.config['Config']['interval'] = int(interval)
			self.save_config()
		except ValueError:
			raise

	def get_password(self):
		return self.config['Config']['password']

	def set_password(self, pw):
		self.config['Config']['password'] = pw
		self.save_config()
		
	def get_dbname(self):
		return self.config['Config']['dbname']
		
	def get_dbuser(self):
		return self.config['Config']['dbuser']
		
	def get_dbpw(self):
		return self.config['Config']['dbpw']
		
	def get_dbhost(self):
		return self.config['Config']['dbhost']


