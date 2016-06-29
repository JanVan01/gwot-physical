#!/usr/bin/python3

import sys
assert sys.version_info >= (3,0)

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from controller.data import DataController
from controller.location import LocationController
from controller.sensor import SensorController
from controller.config import ConfigController
from utils.utils import OS


OS().cwd(__file__)
app = Flask(__name__)
auth = HTTPBasicAuth()

@app.route('/api/1.0/data/trigger')
@auth.login_required
def data_trigger():
	return DataController().trigger()

@app.route('/api/1.0/data/last')
def data_last():
	return DataController().last()

@app.route('/api/1.0/data/list')
def data_list():
	return DataController().list()

@app.route('/api/1.0/data/min')
def data_min():
	return DataController().min()

@app.route('/api/1.0/data/max')
def data_max():
	return DataController().max()

@app.route('/api/1.0/location/list')
def location_list():
	return LocationController().list()

@app.route('/api/1.0/sensor/list')
def sensor_list():
	return SensorController().list()

@app.route('/api/1.0/config', methods=['GET', 'PUT'])
@auth.login_required
def config_config():
    return ConfigController().complete_config()

@app.route('/api/1.0/config/location', methods=['GET', 'PUT', 'POST'])
@auth.login_required
def config_location():
	return ConfigController().location()

@app.route('/api/1.0/config/sensor', methods=['GET', 'PUT', 'POST'])
@auth.login_required
def config_sensor():
	return ConfigController().sensor()

@app.route('/api/1.0/config/password', methods=['GET', 'PUT', 'POST'])#GET for edit password html
@auth.login_required
def config_password():
	return ConfigController().password()

@app.route('/api/1.0/overview')  #Delete it, just for testing c3js.
def data_overview():
	return DataController().overview()

@auth.get_password
def get_password(username):
	return ConfigController().check_password(username)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
