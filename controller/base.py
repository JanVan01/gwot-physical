import importlib
from views.json import JsonView
from views.html import HtmlView
from flask import request

class BaseController(object):

	def get_view(self, template_file = None):
		if self.__is_json_request():
			view = JsonView()
		else:
			view = HtmlView()
		if template_file is not None:
			view.set_template(template_file)
		return view


	def get_model(self, module_name, class_name):
		if module_name is None or class_name is None:
			return None

		try:
			module = importlib.import_module(module_name)
			class_ = getattr(module, class_name)
			return class_()
		except:
			raise # A wrong model is an error we can't really handle here. Abort execution.

	def __is_json_request(self):
		best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
		return best == 'application/json' and request.accept_mimetypes[best] > request.accept_mimetypes['text/html']
