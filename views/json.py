import json
from datetime import datetime
from models.measurements import Measurement
from models.locations import Location
from models.sensors import Sensor
from views.base import BaseView

class JsonView(BaseView):

	def __init__(self):
		super().__init__('application/json')

	def _parse_template(self, data):
		obj = JSON()
		return obj.build(data)
	

	
class JSON(object):

	def build(self, data):
		return json.dumps(data, default=self.__json_serial)

	# JSON serializer for objects not serializable by default json code
	def __json_serial(self, obj):
		if isinstance(obj, datetime):
			return obj.isoformat()

		elif isinstance(obj, Measurement):
			sensor = obj.get_sensor_object()
			return {
				'id': obj.get_id(),
				'datetime': obj.get_datetime(),
				'value': obj.get_value(),
				'quality': obj.get_quality(),
				'sensor': {
					'id': sensor.get_id(),
					'type': sensor.get_type(),
					'unit': sensor.get_unit(),
				},
				'location': {
					'id': obj.get_location()
				}
			}

		elif isinstance(obj, Location):
			return {
				'id': obj.get_id(),
				'name': obj.get_name(),
				'coords': obj.get_position(),
				'height': obj.get_height()
			}

		elif isinstance(obj, Sensor):
			return {
				'id': obj.get_id(),
				'type': obj.get_type(),
				'description': obj.get_description(),
				'unit': obj.get_unit(),
				'active': obj.is_active()
			}
	
		raise TypeError ("Type not serializable")