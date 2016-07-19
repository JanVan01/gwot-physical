class BaseNotifier(object):

	def prepare(self):
		return

	def send(self, notifier, subscriber, measurement):
		return
	
	def is_public(self):
		return False
	
	def get_subscriber_settings(self):
		return [] # Must be unique for both get_subscriber_settings and get_notifier_settings
	
	def get_notifier_settings(self):
		return [] # Must be unique for both get_subscriber_settings and get_notifier_settings
	
	def get_setting_name(self, key):
		return None
	
	def validate_setting(self, key, value):
		return False
	
	def get_setting_html(self, key, value = None):
		return None
		
	def get_setting(self, key):
		if self.settings is not None and key in self.settings:
			return self.settings[key]
		else:
			return None

	def get_settings(self):
		if self.settings is None:
			return {}
		else:
			return self.settings

	def set_settings(self, settings):
		self.settings = settings