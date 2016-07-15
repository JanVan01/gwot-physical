#!/usr/bin/python3

import sys
assert sys.version_info >= (3,0)

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from controller.data import DataController
from controller.location import LocationController
from controller.sensor import SensorController
from controller.config import ConfigController
from controller.frontend import FrontendController
from utils.utils import OS
from views.json import JSON
from models.config import ConfigManager


OS().cwd(__file__)
app = Flask(__name__)
auth = HTTPBasicAuth()

@app.route('/')
def frontend_home():
	return FrontendController().home()

@app.route('/data')
def frontend_data():
	return FrontendController().data()

@app.route('/config')
def frontend_config():
	return FrontendController().config()

@app.route('/config/password')
def frontend_config_password():
	return FrontendController().config_password()

@app.route('/config/sensors')
def frontend_config_sensors():
	return FrontendController().config_sensors()


@app.route('/config/locations')
def frontend_config_locations():
	return FrontendController().config_locations()

@app.route('/about')
def frontend_about():
	return FrontendController().about()

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

@app.route('/api/1.0/sensor/<int:id>/subscription', methods=['GET', 'POST', 'DELETE'])
def sensor_subscription(id):
	return SensorController().subscription(id)

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

@auth.get_password
def get_password(username):
	return ConfigController().check_password(username)

@app.template_filter('json2table')
def json2table(data):
	return JSON().to_table(data)

@app.template_filter('json')
def to_json(data):
	return JSON().build(data)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=ConfigManager.Instance().get_port())
