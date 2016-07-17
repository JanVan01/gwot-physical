from controller.base import BaseController
from flask import request
from models.config import ConfigManager
from utils.utils import Validate


class ConfigController(BaseController):

    def __init__(self):
        super().__init__()
        self.config = ConfigManager.Instance()
        self.validate = Validate()

    def complete_config(self):
        if (request.method == 'GET'):
            data = {}
            data['name'] = self.config.get_name()
            data['interval'] = self.config.get_interval()
            data['location'] = self._get_location(self.config.get_location())

            return self.get_view(template_file='config.html').data(data)
        elif (request.method == 'PUT'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            # TODO(react to invalid input)
            if ('name' in input and input['name'] != ''):
                self.config.set_name(input['name'])
            if ('interval' in input and type(input['interval']) == int):
                self.config.set_interval(input['interval'])
            if ('location' in input and type(input['location']) == int):
                self.config.set_location(input['location'])
            return self.get_view().success()

    def location(self):
        if (request.method == 'GET'):
            data = {}
            return self.get_view(template_file='location_form.html').data(data)
        elif (request.method == 'PUT'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            location = self.get_model('models.locations', 'Location')
            if('id' in input):
                try:
                    location.set_id(int(input['id']))
                    if('name' in input):
                        location.set_name(str(input['name']))
                    if('lat' in input and 'lon' in input):
                        location.set_position(float(input['lat']), float(input['lon']))
                    if('height' in input):
                        location.set_height(float(input['height']))
                    updated = location.update()
                    if not updated:
                        return self.get_view().bad_request('The location you are trying to update does not exist try to create it instead')
                except TypeError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field set')
            return self.get_view().success()
        elif (request.method == 'POST'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            location = self.get_model('models.locations', 'Location')
            if('name' in input and 'lat' in input and 'lon' in input and 'height' in input):
                try:
                    location.set_name(str(input['name']))
                    location.set_position(float(input['lat']), float(input['lon']))
                    location.set_height(float(input['height']))
                    created = location.create()
                    if not created:
                        return self.get_view().bad_request('The location could not be created')

                except TypeError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field available')
            return self.get_view().success()

    def sensor(self):
        if (request.method == 'PUT'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            sensor = self.get_model('models.sensors', 'Sensor')
            if('id' in input):
                try:
                    sensor.set_id(int(input['id']))
                    if('module' in input):
                        sensor.set_module(str(input['module']))
                    if ('class_name' in input):
                        sensor.set_class(str(input['class_name']))
                    if ('type' in input):
                        sensor.set_type(str(input['type']))
                    if ('description' in input):
                        sensor.set_description(str(input['description']))
                    if('unit' in input):
                        sensor.set_unit(str(input['unit']))
                    if ('active' in input):
                        sensor.set_active(bool(input['active']))
                    updated = sensor.update()
                    if not updated:
                        return self.get_view().bad_request('The sensor you are trying to update does not exist try to create it instead')
                except TypeError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field set')
            return self.get_view().success()
        elif (request.method == 'POST'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            sensor = self.get_model('models.sensors', 'Sensor')
            if('type' in input and 'description' in input and
                    'unit' in input and 'active' in input and
                    'module' in input and 'class_name' in input):
                try:
                    sensor.set_module(str(input['module']))
                    sensor.set_class(str(input['class_name']))
                    sensor.set_type(str(input['type']))
                    sensor.set_description(str(input['description']))
                    sensor.set_unit(str(input['unit']))
                    sensor.set_active(bool(input['active']))
                    updated = sensor.update()
                    if not updated:
                        return self.get_view().bad_request('The sensor you are trying to update does not exist try to create it instead')
                except TypeError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field set')
            return self.get_view().success()

    def password(self):
        input = request.get_json()
        if(input is None):
            return self.get_view().bad_request('expected json')
        self.config.set_password(input['password'])
        return self.get_view().success()

    def check_password(self, username):
        if username == "admin":
            return self.config.get_password()
        return None

    def _get_location(self, id):
        location_model = self.get_model('models.locations', 'Location')
        location_model.set_id(id)
        location_model.read()
        location = {}
        location['id'] = location_model.get_id()
        location['name'] = location_model.get_name()
        location['lat'] = location_model.get_latitude()
        location['lon'] = location_model.get_longitude()
        location['height'] = location_model.get_height()
        return location
