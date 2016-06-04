from views.base import BaseView
from flask import render_template

class HtmlView(BaseView):

	def __init__(self):
		super().__init__('text/html')

	def _parse_template(self, data):
		if self.template is not None:
			template = self.template
		else:
			template = "default.html"
		return render_template(template, data=data)
