from lindshop.core.breadcrumbs.breadcrumbs import Breadcrumbs
class BreadcrumbsMixin(object):
	"""Add Breadcrumbs to the context of the page
	"""
	def get_context_data(self, **kwargs):
		context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)

		breadcrumbs = Breadcrumbs()
		breadcrumbs.add(self.object)

		context['breadcrumbs'] = breadcrumbs.crumbs

		return context