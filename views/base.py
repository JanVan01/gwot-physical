from flask import Response

class BaseView(object):

	def __init__(self, mine_type):
		self.mine_type = mine_type;
		self.template = None
		
	def set_template(self, file):
		self.template = file

	def data(self, data):
		return self._send_data(200, data);
	
	def success(self):
		return self._send_empty(204);
	
	def error(self):
		return self._send_empty(500);

	def notfound(self):
		return self._send_empty(404);

	def forbidden(self):
		return self._send_empty(403);
	
	def _send_empty(self, httpcode):
		return Response('', status=httpcode, mimetype=self.mine_type)

	def _send_data(self, httpcode, data):
		return Response(self._parse_template(data), status=httpcode, mimetype=self.mine_type)

	def _parse_template(self, data):
		return data