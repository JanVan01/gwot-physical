class BaseNotifier(object):

	def send(self, notifier, subscriber, measurement):
		return
	
	def is_public(self):
		return False
	
	def get_subscriber_settings(self):
		return {} # Must be unique for both get_subscriber_settings and get_notifier_settings
	
	def get_notifier_settings(self):
		return {} # Must be unique for both get_subscriber_settings and get_notifier_settings
	
	def get_setting_name(self, key):
		return None
	
	def validate_setting(self, key, value):
		return False
	
	def get_setting_html(self, key, value):
		return None
	
	def _get_input_field(self, key, value):
		return "<input type='text' name='"+key+"' value='"+self._htmlspecialchars(value)+"' />"
	
	def _htmlspecialchars(self, value):
		value.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")
		return value