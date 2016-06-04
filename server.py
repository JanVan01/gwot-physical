import sys
assert sys.version_info >= (3,0)

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from controller.data import DataController
from controller.location import LocationController
from controller.sensor import SensorController
from controller.config import ConfigController

app = Flask(__name__)
auth = HTTPBasicAuth()

@app.route('/api/data/trigger')
@auth.login_required
def data_trigger():
	return DataController().trigger()

@app.route('/api/data/last')
def data_last():
	return DataController().last()

@app.route('/api/data/list')
def data_list():
	return DataController().list()

@app.route('/api/data/min')
def data_min():
	return DataController().min()

@app.route('/api/data/max')
def data_max():
	return DataController().max()

@app.route('/api/location/list')
def location_list():
	return LocationController().list()

@app.route('/api/sensor/list')
def sensor_list():
	return SensorController().list()

@app.route('/api/config/name', methods=['GET', 'PUT'])
@auth.login_required
def config_name():
	return ConfigController().name()

@app.route('/api/config/height', methods=['GET', 'PUT'])
@auth.login_required
def config_height():
	return ConfigController().height()

@app.route('/api/config/location', methods=['GET', 'PUT', 'POST', 'DELETE'])
@auth.login_required
def config_location():
	return ConfigController().location()

@app.route('/api/config/interval', methods=['GET', 'PUT'])
@auth.login_required
def config_interval():
	return ConfigController().interval()

@app.route('/api/config/password', methods=['GET', 'PUT'])
@auth.login_required
def config_password():
	return ConfigController().password()

@app.route('/api/config/sensor', methods=['GET', 'PUT', 'POST', 'DELETE'])
@auth.login_required
def config_sensor():
	return ConfigController().sensor()


@auth.get_password
def get_password(username):
	return ConfigController().check_password(username)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
