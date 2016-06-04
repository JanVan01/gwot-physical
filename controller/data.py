from flask import request
from models.sensor import Sensor
from controller.base import BaseController

class DataController(BaseController):

	def __init(self):
		BaseController.__init__(self);
		self.sensor = Sensor()
	
	def trigger(self):
		location = 1 # ToDO: to be set properly
		value = self.sensor.trigger_reading()
		data = self.db.save_measurement(value, location)
		return self.get_view().data(data)
	
	def last(self):
		data = self.db.get_last_measurement(self._get_filter())
		return self.get_view().data(data)
		
	def list(self):
		data = self.db.get_measurement_list(self._get_filter())
		return self.get_view().data(data)
		
	def min(self):
		data = self.db.get_min_measuremen(self._get_filter())
		return self.get_view().data(data)
		
	def max(self):
		data = self.db.get_max_measurement(self._get_filter())
		return self.get_view().data(data)

	def _get_filter(self):
		# ToDo: Add proper variable checks / sanitation
		outliers = request.args.get('outliers')
		start = request.args.get('start')
		end = request.args.get('end')
		location = request.args.get('location')
		coordinates = request.args.get('coordinates')

		args = {
			'outliers': None,
			'start': None,
			'end': None,
			'location': None,
			'coordinates': None
		}

		if outliers != None and len(outliers) > 0 and (outliers == 0 or outliers == 1):
			args['outliers'] = outliers

		# ToDo
		if start != None and len(start) > 0:
			args['start'] = start

		# ToDo
		if end != None and len(end) > 0:
			args['end'] = end

		if location != None and location > 0:
			args['location'] = location

		# ToDo
		if coordinates != None and len(coordinates) > 0:
			args['coordinates'] = coordinates

		return args

