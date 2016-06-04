from controller.base import BaseController

class LocationController(BaseController):
		
	def list(self):
		model = self.get_model('models.locations', 'Locations')
		data = model.get_all()
		return self.get_view().data(data)