from flask import request
from controller.base import BaseController
from Notification import publishEveryMeasurement
class DataController(BaseController):

	def __init__(self):
		super().__init__()
		self.multi_model = self.get_model('models.measurements', 'Measurements')

	def trigger(self):
		sensors = self.get_model('models.sensors', 'Sensors')
		data = sensors.trigger_all()
		publishEveryMeasurement("HELLO") # should pass data to mqttbroker
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

		args = self.multi_model.filter_defaults()

		outliers = request.args.get('outliers')
		if outliers != None and len(outliers) > 0 and (outliers == 0 or outliers == 1):
			args['outliers'] = outliers

		# ToDo
		start = request.args.get('start')
		if start != None and len(start) > 0:
			args['start'] = start

		# ToDo
		end = request.args.get('end')
		if end != None and len(end) > 0:
			args['end'] = end

		# ToDo
		location = request.args.get('location')
		if location != None and len(location) > 0:
			args['location'] = location.split(',')

		# ToDo
		sensor = request.args.get('sensor')
		if sensor != None and len(sensor) > 0:
			args['location'] = sensor.split(',')

		# ToDo, WKT parsing using https://github.com/larsbutler/geomet
		coordinates = request.args.get('coordinates')
		if coordinates != None and len(coordinates) > 0:
			args['coordinates'] = coordinates

		return args
