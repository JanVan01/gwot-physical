from views.base import BaseView
from flask import render_template
from models.config import ConfigManager

class HtmlView(BaseView):

	def __init__(self):
		super().__init__('text/html')

	def _parse_template(self, data):
		if self.template is not None:
			template = self.template
		else:
			template = "default.html"
		return render_template(template, data = data, config = ConfigManager.Instance())
