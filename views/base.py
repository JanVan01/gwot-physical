from flask import Response

class BaseView(object):

	def __init__(self, mine_type):
		self.mine_type = mine_type
		self.template = None

	def set_template(self, file):
		self.template = file

	def data(self, data = {}):
		return self._send_data(200, data)

	def success(self):
		return self._send_empty(204)

	def error(self):
		return self._send_empty(500)

	def notfound(self):
		return self._send_empty(404)

	def forbidden(self):
		return self._send_empty(403)

	def bad_request(self, message):
		return self._send_message(400, message)

	def _send_empty(self, httpcode):
		return Response('', status=httpcode, mimetype=self.mine_type)

	def _send_data(self, httpcode, data):
		return Response(self._parse_template(data), status=httpcode, mimetype=self.mine_type)

	def _send_message(self, httpcode, message):
		return Response(message, status=httpcode, mimetype=self.mine_type)

	def _parse_template(self, data):
		return data
