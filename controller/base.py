from models.database import Database
from views.json import JsonView
from views.html import HtmlView
from flask import request

class BaseController(object):

	def __init__(self):
		self.db = Database()
		
	def get_view(self, template_file = None):
		if self.__is_json_request():
			view = JsonView()
		else:
			view = HtmlView()
		if template_file is None:
			view.set_template(template_file)
		return view
	
	def __is_json_request(self):
		best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
		return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
