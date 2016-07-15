from flask import request
from controller.base import BaseController
from utils.utils import Validate

class DataController(BaseController):

	def __init__(self):
		super().__init__()
		self.multi_model = self.get_model('models.measurements', 'Measurements')

	def trigger(self):
		sensors = self.get_model('models.sensors', 'Sensors')
		data = sensors.trigger_all()
		return self.get_view().data(data)

	def last(self):
		data = self.multi_model.get_last(self._get_filter())
		return self.get_view().data(data)

	def list(self):
		data = self.multi_model.get_all(self._get_filter())
		return self.get_view().data(data)

	def min(self):
		data = self.multi_model.get_min(self._get_filter())
		return self.get_view().data(data)

	def max(self):
		data = self.multi_model.get_max(self._get_filter())
		return self.get_view().data(data)

	def avg(self):
		data = self.multi_model.get_avg(self._get_filter())
		return self.get_view().data(data)

	def overview(self): # Testing pretty Dataview.
		data = self.multi_model.get_all(self._get_filter())
		return self.get_view(template_file = "index.html").data(data)

	def _get_filter(self):
		valid = Validate()
		args = {}

		start = request.args.get('start')
		if valid.iso_timestamp(start):
			args['start'] = start

		end = request.args.get('end')
		if valid.iso_timestamp(end):
			args['end'] = end

		location = request.args.get('location')
		if valid.comma_separated_numbers(location):
			args['location'] = location.split(',')

		sensor = request.args.get('sensor')
		if valid.comma_separated_numbers(sensor):
			args['sensor'] = sensor.split(',')

		geometry = request.args.get('geometry')
		if valid.wkt(geometry):
			args['geometry'] = geometry

		limit = request.args.get('limit')
		if valid.integer(limit) and int(limit) > 0:
			args['limit'] = int(limit)

		return args
