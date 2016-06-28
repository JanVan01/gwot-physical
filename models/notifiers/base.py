class BaseNotifier(object):
	
	def __init__(self, data):
		self.data = data

	def single(self):
		return None
	
	def byThreshold(self):
		return None;

	
class BaseNotifier(object):

	def new(self, data):
		notification = Notification(data)
		data.single()
		if 1==1:
			data.byThreshold()
			
	def send(self, data):
		thread = MyThread()
		thread.daemon = True
		thread.start()
			
class MyThread(threading.Thread):
	def run(self):
		'''Start your thread here'''
		pass