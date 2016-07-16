import os
import re
import psycopg2
import psycopg2.extras
import importlib
from utils.singleton import Singleton
from models.config import ConfigManager
from pygeoif import geometry

class OS:
	
	def cwd(self, filepath):
		abspath = os.path.abspath(filepath)
		dname = os.path.dirname(abspath)
		os.chdir(dname)
		
	def create_object(self, module_name, class_name):
		if module_name is None or class_name is None:
			return None
		
		try:
			module = importlib.import_module(module_name)
			class_ = getattr(module, class_name)
			return class_()
		except:
			print("Can't create object " + module_name + "." + class_name)
			return None


@Singleton
class Database:
	
	def __init__(self):
		config = ConfigManager.Instance()
		self.db = psycopg2.connect("dbname='" + config.get_dbname() + "' user='" + config.get_dbuser() + "' host='" + config.get_dbhost() + "' password='" + config.get_dbpw() + "'")
		self.db.autocommit = True # We might want to remove that and switch to transactions
	
	def get(self):
		return self.db
	
	def dict_cursor(self):
		return self.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
	
	def cursor(self):
		return self.db.cursor()

class Validate:
	
	def __init__(self):
		# Source: http://stackoverflow.com/questions/28020805/regex-validate-correct-iso8601-date-string-with-time
		self.iso_regex = '^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29)((T|\s)(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d))?$'
	
	def comma_separated_numbers(self, data):
		if data is None or len(data) == 0:
			return False

		list = data.split(',')
		for entry in list:
			if not entry.isdigit():
				return False

		return True
		
	def iso_timestamp(self, data):
		if data is None or len(data) == 0:
			return False
		
		if re.match(self.iso_regex, data) is None:
			return False
		
		return True
	
	def integer(self, data):
		if data is None or len(data) == 0:
			return False
		else:
			return data.isdigit()
		
	def wkt(self, data):
		if data is None or len(data) == 0:
			return False

		try:
			wkt = geometry.from_wkt(data)
			return isinstance(wkt, geometry._Geometry)
		except:
			return False

class SettingManager:
	
	def get_input_field(self, key, value):
		return "<input type='text' name='"+key+"' value='"+self._htmlspecialchars(value)+"' />"
	
	def htmlspecialchars(self, value):
		value.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")
		return value