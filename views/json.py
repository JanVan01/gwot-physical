import json
from datetime import datetime, timedelta
from models.measurements import Measurement
from models.locations import Location
from models.sensors import Sensor
from views.base import BaseView
from json2table import convert

class JsonView(BaseView):

	def __init__(self):
		super().__init__('application/json')

	def _parse_template(self, data):
		obj = JSON()
		return obj.build(data)
	

	
class JSON(object):

	def build(self, data):
		return json.dumps(data, default=self.__json_serial)
	
	def parse(self, data):
		return json.loads(data)
	
	def to_table(self, data):
		# Work around bugs in json2table:
		if not isinstance(data, dict):
			datatype = type(data)
			if isinstance(data, list) and len(data) > 0:
				datatype = type(data[0])
			temp = {}
			temp[datatype.__name__] = data
			data = temp
		# This is an ugly hack to expand the objects:
		data = self.parse(self.build(data))
		# Finally convert json data to a table:
		return convert(data, build_direction="TOP_TO_BOTTOM", table_attributes={"class" : "table"})

	# JSON serializer for objects not serializable by default json code
	def __json_serial(self, obj):
		if isinstance(obj, datetime):
			return obj.isoformat()
		
		elif isinstance(obj, timedelta):
			return str(obj)

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