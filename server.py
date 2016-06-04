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
	controller = DataController()
	return controller.trigger()

@app.route('/api/data/last')
def data_last():
	controller = DataController()
	return controller.last()

@app.route('/api/data/list')
def data_list():
	controller = DataController()
	return controller.list()

@app.route('/api/data/min')
def data_min():
	controller = DataController()
	return controller.min()

@app.route('/api/data/max')
def data_max():
	controller = DataController()
	return controller.max()

@app.route('/api/location/list')
def location_list():
	controller = LocationController()
	return controller.list()

@app.route('/api/sensor/list')
def sensor_list():
	controller = SensorController()
	return controller.list()

@app.route('/api/config/name', methods=['GET', 'PUT'])
@auth.login_required
def config_name():
	controller = ConfigController()
	return controller.name()

@app.route('/api/config/height', methods=['GET', 'PUT'])
@auth.login_required
def config_height():
	controller = ConfigController()
	return controller.height()

@app.route('/api/config/location', methods=['GET', 'PUT', 'POST', 'DELETE'])
@auth.login_required
def config_location():
	controller = ConfigController()
	return controller.location()

@app.route('/api/config/interval', methods=['GET', 'PUT'])
@auth.login_required
def config_interval():
	controller = ConfigController()
	return controller.interval()

@app.route('/api/config/password', methods=['GET', 'PUT'])
@auth.login_required
def config_password():
	controller = ConfigController()
	return controller.password()

@app.route('/api/config/sensor', methods=['GET', 'PUT', 'POST', 'DELETE'])
@auth.login_required
def config_sensor():
	controller = ConfigController()
	return controller.sensor()


@auth.get_password
def get_password(username):
	controller = ConfigController()
	return controller.check_password(username)


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
