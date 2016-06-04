from flask import request
from controller.base import BaseController

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
		data = self.multi_model.get_all_filtered(self._get_filter())
		return self.get_view().data(data)
		
	def min(self):
		data = self.multi_model.get_min(self._get_filter())
		return self.get_view().data(data)
		
	def max(self):
		data = self.multi_model.get_max(self._get_filter())
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

