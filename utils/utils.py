import os
import psycopg2
from models.config import ConfigManager

class OS:
	
	def cwd(self, filepath):
		abspath = os.path.abspath(filepath)
		dname = os.path.dirname(abspath)
		os.chdir(dname)


class Database:
	
	def connect(self):
		config = ConfigManager()
		db = psycopg2.connect("dbname='" + config.get_dbname() + "' user='" + config.get_dbuser() + "' host='" + config.get_dbhost() + "' password='" + config.get_dbpw() + "'")
		db.autocommit = True # We might want to remove that and switch to transactions
		return db
		