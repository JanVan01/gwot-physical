from controller.base import BaseController

from models.locations import Locations

class LocationController(BaseController):
		
	def list(self):
		data = Locations().get_all()
		return self.get_view().data(data)