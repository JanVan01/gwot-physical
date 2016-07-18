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
from utils.utils import OS, ThreadObserver
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
@auth.login_required
def frontend_config():
	return FrontendController().config()

@app.route('/config/password')
@auth.login_required
def frontend_config_password():
	return FrontendController().config_password()

@app.route('/config/sensors')
@auth.login_required
def frontend_config_sensors():
	return FrontendController().config_sensors()

@app.route('/config/sensors/add', defaults={'id': None, 'mode': 'add'}, methods=['GET', 'POST'])
@app.route('/config/sensors/edit/<int:id>', defaults={'mode': 'edit'})
@auth.login_required
def frontend_config_sensors_change(mode, id):
	print(id)
	return FrontendController().config_sensors_change(mode, id)

@app.route('/config/locations')
@auth.login_required
def frontend_config_locations():
	return FrontendController().config_locations()

@app.route('/config/locations/add', defaults={'id': None, 'mode': 'add'})
@app.route('/config/locations/edit/<int:id>', defaults={'mode': 'edit'})
@auth.login_required
def frontend_config_locations_change(mode, id):
	return FrontendController().config_locations_change(mode, id)

@app.route('/config/notifications')
@auth.login_required
def frontend_config_notifications():
	return FrontendController().config_notifications()

@app.route('/config/notifications/add', defaults={'id': None, 'mode': 'add'}, methods=['GET', 'POST'])
@app.route('/config/notifications/edit/<int:id>', defaults={'mode': 'edit'})
@auth.login_required
def frontend_config_notifications_change(mode, id):
	return FrontendController().config_notifications_change(mode, id)

@app.route('/config/notifications/<int:id>/subscriptions')
@auth.login_required
def frontend_config_subscriptions(id):
	return FrontendController().config_subscriptions(id)

@app.route('/config/subscriptions/add', defaults={'sid': None, 'mode': 'add'})
@app.route('/config/subscriptions/edit/<int:sid>', defaults={'mode': 'edit'})
@auth.login_required
def frontend_config_subscriptions_change(mode, nid, sid):
	return FrontendController().config_subscriptions_change(mode, nid, sid)

@app.route('/tutorial/notifications')
def frontend_tutorial_notifications():
	return FrontendController().tutorial_notifications()

@app.route('/tutorial/sensors')
def frontend_tutorial_sensors():
	return FrontendController().tutorial_sensors()

@app.route('/about')
def frontend_about():
	return FrontendController().about()

@app.route('/subscriptions')
def frontend_subscriptions():
	return FrontendController().subscriptions()

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

@app.route('/api/1.0/data/trend')
def data_trend():
	return DataController().trend()

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

@app.route('/api/1.0/config/location/<int:id>', methods=['DELETE'])
@app.route('/api/1.0/config/location', defaults={'id': None}, methods=['PUT', 'POST'])
@auth.login_required
def config_location(id):
	return ConfigController().location(id)

@app.route('/api/1.0/config/sensor/<int:id>', methods=['DELETE'])
@app.route('/api/1.0/config/sensor', defaults = {'id': None}, methods=['PUT', 'POST'])
@auth.login_required
def config_sensor(id):
	return ConfigController().sensor(id)

@app.route('/api/1.0/config/notification/<int:id>', methods=['DELETE'])
@app.route('/api/1.0/config/notification', defaults = {'id': None}, methods=['PUT', 'POST'])
@auth.login_required
def config_notification(id):
	return ConfigController().notification(id)

@app.route('/api/1.0/config/subscription/<int:id>', methods=['DELETE'])
@app.route('/api/1.0/config/subscription', defaults = {'id': None}, methods=['PUT', 'POST'])
@auth.login_required
def config_subscription(id):
	return ConfigController().subscription(id)

@app.route('/api/1.0/config/password', methods=['PUT'])
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

@app.after_request
def after_request(response):
	ThreadObserver.Instance().wait();
	return response

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=ConfigManager.Instance().get_port())
