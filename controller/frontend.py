from controller.base import BaseController
from views.html import HtmlView
import time

class FrontendController(BaseController):

	def __init__(self):
		super().__init__()
		self.multi_model = self.get_model('models.measurements', 'Measurements')

	def get_view(self, template_file=None):
		view = HtmlView()
		if template_file is not None:
			view.set_template(template_file)
		return view

	def home(self):
		location = 1
		sensor = 1
		data = {
			"minYearly": self.__getminmaxvalue(time.strftime("%Y-01-01T00:00:00Z"), location, sensor),
			"maxYearly": self.__getminmaxvalue(time.strftime("%Y-01-01T00:00:00Z"), location, sensor, False),
			"minHourly": self.__getminmaxvalue(time.strftime("%Y-%m-%dT%H:00:00Z"), location, sensor),
			"maxHourly": self.__getminmaxvalue(time.strftime("%Y-%m-%dT%H:00:00Z"), location, sensor, False)
		}
		return self.get_view('index.html').data(data)
	
	def __getminmaxvalue(self, start, location, sensor, min = True):
		filterObj = {
			'start': start,
			'location': [str(location)],
			'sensor': [str(sensor)],
			'limit': 1
		}
		if min is True:
			mlist = self.multi_model.get_min(filterObj)
		else:
			mlist = self.multi_model.get_max(filterObj)
		if len(mlist) == 0:
			return "None"
		else:
			return str(mlist[0].get_value())

	def config(self):
		data = {}
		return self.get_view('config.html').data(data)

	def config_password(self):
		data = {}
		return self.get_view('config_password.html').data(data)

	def config_sensors(self):
		data = {}
		return self.get_view('config_sensors.html').data(data)

	def config_locations(self):
		data = {}
		return self.get_view('config_locations.html').data(data)

	def data(self):
		data = self.multi_model.get_all()
		return self.get_view('data.html').data(data)

	def about(self):
		data = {}
		return self.get_view('about.html').data(data)
