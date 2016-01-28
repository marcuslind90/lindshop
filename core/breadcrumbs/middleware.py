import lindshop.core.breadcrumbs as hc
from lindshop.core.breadcrumbs import CrumbedView

class CrumbsMiddleware(object):
	def process_view(self, request, view_func, view_args, view_kwargs):
		self._view = CrumbedView(view_func, request.path, view_args, view_kwargs) if hc.is_crumbed(view_func) else None

	def process_template_response(self, request, response):
		if self._view is None:
			return response

		p = self._view
		view_path = []
		while (p is not None):
			view_path.append(p.as_dict())
			p = p.parent

		if response.context_data is None:
			response.context_data = {}
		print "View Path is :%s" % view_path
		response.context_data['crumbs'] = reversed(view_path)
		return response