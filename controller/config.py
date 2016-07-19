from controller.base import BaseController
from flask import request
from models.config import ConfigManager
from models.locations import Locations
from models.notifiers import Notifiers
from models.sensors import Sensors
from models.subscribers import Subscribers
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
            try:
                if ('name' in input):
                    self.config.set_name(str(input['name']))
                if ('interval' in input):
                    self.config.set_interval(int(input['interval']))
                if ('location' in input):
                    self.config.set_location(int(input['location']))
            except ValueError:
                return self.get_view().bad_request('Input not in the right format')
            return self.get_view().success()

    def location(self, id):
        if (request.method == 'DELETE'):
            location = Locations().get(id)
            if location is None:
                return self.get_view().bad_request('Location does not exist')
            if location.delete():
                return self.get_view().success()
            else:
                return self.get_view().error()
        elif (request.method == 'PUT'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            if('id' in input):
                location = Locations().get(int(input['id']))
                if location is None:
                    return self.get_view().bad_request('The sensor you are trying to update does not exist try to create it instead')
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
                except ValueError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field set')
            return self.get_view().success()
        elif (request.method == 'POST'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            if('name' in input and 'lat' in input and 'lon' in input and 'height' in input):
                location = Locations().create()
                try:
                    location.set_name(str(input['name']))
                    location.set_position(float(input['lat']), float(input['lon']))
                    location.set_height(float(input['height']))
                    created = location.create()
                    if not created:
                        return self.get_view().bad_request('The location could not be created')
                except ValueError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field available')
            return self.get_view().success()

    def sensor(self, id):
        if (request.method == 'DELETE'):
            sensor = Sensors().get(id)
            if sensor is None:
                return self.get_view().bad_request('Location does not exist')
            if sensor.delete():
                return self.get_view().success()
            else:
                return self.get_view().error()
        elif (request.method == 'PUT'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            if('id' in input):
                try:
                    sensor = Sensors().get(int(input['id']))
                    if sensor is None:
                        return self.get_view().bad_request('The sensor you are trying to update does not exist try to create it instead')
                    if 'module' in input:
                        sensor.set_module(str(input['module']))
                    if 'class_name' in input:
                        sensor.set_class(str(input['class_name']))
                    if 'description' in input:
                        sensor.set_description(str(input['description']))
                    if 'settings' in input:
                        sensor.set_settings(input['settings'])
                    if 'active' in input:
                        sensor.set_active(bool(input['active']))
                    if not sensor.update():
                        return self.get_view().bad_request('The sensor you are trying to update does not exist try to create it instead')
                except ValueError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field set')
            return self.get_view().success()
        elif (request.method == 'POST'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            if ('description' in input and 'module' in input and 'class_name' in input
                    and 'active' in input and 'settings' in input):
                sensor = Sensors().create()
                try:
                    sensor.set_module(str(input['module']))
                    sensor.set_class(str(input['class_name']))
                    sensor.set_description(str(input['description']))
                    sensor.set_settings(input['settings'])
                    sensor.set_active(bool(input['active']))
                    if not sensor.create():
                        return self.get_view().bad_request('The sensor you are trying to update does not exist try to create it instead')
                except ValueError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field set')
            return self.get_view().success()

    def notification(self, id):
        if (request.method == 'DELETE'):
            notification = Notifiers().get(id)
            if notification is None:
                return self.get_view().bad_request('Location does not exist')
            if notification.delete():
                return self.get_view().success()
            else:
                return self.get_view().error()
        elif (request.method == 'PUT'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            if('id' in input):
                try:
                    notification = Notifiers().get(int(input['id']))
                    if notification is None:
                        return self.get_view().bad_request('The Notification you are trying to update does not exist try to create it instead')
                    if 'module' in input:
                        notification.set_module(str(input['module']))
                    if 'class_name' in input:
                        notification.set_class(str(input['class_name']))
                    if 'description' in input:
                        notification.set_description(str(input['description']))
                    if 'settings' in input:
                        notification.set_settings(input['settings'])
                    if 'active' in input:
                        notification.set_active(bool(input['active']))
                    if not notification.update():
                        return self.get_view().bad_request('The Notification you are trying to update does not exist try to create it instead')
                except ValueError:
                    return self.get_view().bad_request('Input not in the right format')
            else:
                return self.get_view().bad_request('Not all necessary field set')
            return self.get_view().success()
        elif (request.method == 'POST'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('Expected json')
            if ('description' in input and 'module' in input and 'class_name' in input
                    and 'active' in input and 'settings' in input):
                notification = Notifiers().create()
                try:
                    notification.set_module(str(input['module']))
                    notification.set_class(str(input['class_name']))
                    notification.set_description(str(input['description']))
                    notification.set_settings(input['settings'])
                    notification.set_active(bool(input['active']))
                    if not notification.create():
                        return self.get_view().bad_request('The notification you are trying to update does not exist try to create it instead')
                except ValueError:
                    return self.get_view().bad_request('input not in the right format')
            else:
                return self.get_view().bad_request('not all necessary field set')
            return self.get_view().success()

    def subscription(self, id):
        if (request.method == 'DELETE'):
            subscription = Subscribers().get(id)
            if subscription is None:
                return self.get_view().bad_request('Subscription does not exist')
            if subscription.delete():
                return self.get_view().success()
            else:
                return self.get_view().error()
        elif (request.method == 'PUT'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('expected json')
            if('id' in input):
                try:
                    subscription = Subscribers().get(int(input['id']))
                    if subscription is None:
                        return self.get_view().bad_request('The Notification you are trying to update does not exist try to create it instead')
                    if 'notifier' in input:
                        subscription.set_notifier(int(input['notifier']))
                    if 'sensor' in input:
                        subscription.set_sensor(int(input['sensor']))
                    if 'settings' in input:
                        subscription.set_settings(input['settings'])
                    if not subscription.update():
                        return self.get_view().bad_request('The Subscription you are trying to update does not exist try to create it instead')
                except ValueError:
                    return self.get_view().bad_request('Input not in the right format')
            else:
                return self.get_view().bad_request('Not all necessary field set')
            return self.get_view().success()
        elif (request.method == 'POST'):
            input = request.get_json()
            if(input is None):
                return self.get_view().bad_request('Expected json')
            if ('notifier' in input and 'sensor' in input and 'settings' in input):
                subscription = Subscribers().create()
                try:
                    subscription.set_notifier(int(input['notifier']))
                    subscription.set_sensor(int(input['sensor']))
                    subscription.set_settings(input['settings'])
                    if not subscription.create():
                        return self.get_view().bad_request('The subscription you are trying to update does not exist try to create it instead')
                except ValueError:
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
        location_model = Locations().get(id)
        location = {}
        location['id'] = location_model.get_id()
        location['name'] = location_model.get_name()
        location['lat'] = location_model.get_latitude()
        location['lon'] = location_model.get_longitude()
        location['height'] = location_model.get_height()
        return location
