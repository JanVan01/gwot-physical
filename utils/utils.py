import os
import os.path
import re
import psycopg2
import psycopg2.extras
import importlib
import glob
from utils.singleton import Singleton
from models.config import ConfigManager
from pygeoif import geometry
from flask import request
from werkzeug.utils import secure_filename

class OS:
	
	def cwd(self, filepath):
		abspath = os.path.abspath(filepath)
		dname = os.path.dirname(abspath)
		os.chdir(dname)
		
	def create_object(self, module_name, class_name = None):
		if module_name is None:
			return None
		
		if class_name is None:
			parts = module_name.rsplit('.', 1)
			if len(parts) != 2:
				return None
			else:
				module_name = parts[0]
				class_name = parts[1]
		
		try:
			module = importlib.import_module(module_name)
			class_ = getattr(module, class_name)
			return class_()
		except:
			print("Can't create object " + module_name + "." + class_name)
			return None
		
	def get_classes(self, folder, class_suffix, selected = None):
		classes = []
		for file in glob.glob(folder + "/*.py"):
			handle = open(file, "r")
			content = handle.read()
			handle.close()
			
			module = folder.replace('/', '.').replace('\\', '.') + '.' + os.path.basename(file).replace('.py', '')

			regexp = "\sclass\s+([\w\d]+"+class_suffix+")\s*\(([\w\d]*)\)\s*:\s"
			for m in re.finditer(regexp, content):
				parent_class = m.group(2)
				if len(parent_class) == 0 or parent_class == 'object':
					continue
				class_name = m.group(1)
				classes.append(module + '.' + class_name)
				
		return classes
	
	def upload_file(self, folder, param):
		if request.method == 'POST':
			# check if the post request has the file part
			if param not in request.files:
				return None
			file = request.files[param]
			# if user does not select file, browser also submit a empty part without filename
			if not file or len(file.filename) == 0:
				return None
			if '.' in file.filename and file.filename.rsplit('.', 1)[1] == 'py':
				filename = secure_filename(file.filename)
				file.save(os.path.join(folder, filename))
				return filename
		
class Transform:
	
	def round(self, value, precision):
		if precision < 0:
			div = pow(10, abs(precsion))
			temp = value / div
			temp = round(temp)
			value = temp * div
		elif precision == 0:
			value = round(value)
		else:
			value = round(value, precision)
		return value


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
	
	def floating(self, data):
		if data is None or len(data) == 0:
			return False
		try:
			data = float(data)
			return True
		except ValueError:
			return False
		
	def wkt(self, data):
		if data is None or len(data) == 0:
			return False

		try:
			wkt = geometry.from_wkt(data)
			return isinstance(wkt, geometry._Geometry)
		except:
			return False

class SettingManager:
	
	def get_input_field(self, key, value = None):
		if value is None:
			value = ""
		else:
			value = self.htmlspecialchars(value)
		return "<input type='text' id="+key+" name='"+key+"' class='custom-settings form-control' value='"+value+"' />"
	
	def htmlspecialchars(self, value):
		value.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")
		return value
	
@Singleton
class ThreadObserver:
	
	def __init__(self):
		self.threads = []
		
	def add(self, obj):
		self.threads.append(obj)

	def remove(self, obj):
		self.threads.remove(obj)
		
	def wait(self):
		for thread in self.threads:
			thread.join()