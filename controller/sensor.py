from controller.base import BaseController

class SensorController(BaseController):
		
	def list(self):
		model = self.get_model('models.sensors', 'Sensors')
		data = model.get_all()
		return self.get_view().data(data)
	
	def subscription(self, id):
		return None # ToDo