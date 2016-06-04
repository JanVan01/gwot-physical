from controller.base import BaseController

class SensorController(BaseController):

	def __init(self):
		BaseController.__init__(self);
		
	def list(self):
		data = self.db.get_sensor_list()
		return self.get_view().data(data)