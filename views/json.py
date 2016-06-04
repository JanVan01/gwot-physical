import json
from views.base import BaseView

class JsonView(BaseView):

	def __init__(self):
		BaseView.__init__(self, 'application/json')

	def _parse_template(self, data):
		# The "template" is always the same for JSON... the model just return what we need.
		return json.dumps(data, default=self.__json_serial);

	# JSON serializer for objects not serializable by default json code
	def __json_serial(self, obj):
		if isinstance(obj, datetime):
			serial = obj.isoformat()
			return serial
		raise TypeError ("Type not serializable")