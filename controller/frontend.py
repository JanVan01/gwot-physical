from controller.base import BaseController

class FrontendController(BaseController):

	def __init__(self):
		super().__init__()
		self.multi_model = self.get_model('models.measurements', 'Measurements')

	def get_view(self, template_file = None):
		view = HtmlView()
		if template_file is not None:
			view.set_template(template_file)
		return view

	def home(self):
		data = self.multi_model.get_all()
		return self.get_view().data(data)

	def config(self):
		data = self.multi_model.get_all()
		return self.get_view().data(data)

	def config_password(self):
		data = self.multi_model.get_all()
		return self.get_view().data(data)

	def config_sensors(self):
		data = self.multi_model.get_all()
		return self.get_view().data(data)

	def config_locations(self):
		data = self.multi_model.get_all()
		return self.get_view().data(data)

	def data(self):
		data = self.multi_model.get_all()
		return self.get_view().data(data)