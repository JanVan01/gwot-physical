from controller.base import BaseController
from models.sensors import Sensors

class SensorController(BaseController):
		
	def list(self):
		data = Sensors().get_all()
		return self.get_view().data(data)