class Breadcrumbs(object):
	def __init__(self, *args, **kwargs):
		self.crumbs = []

	def add_category(self, category, url=True):
		if category.parent:
			self.add_category(category.parent)  # Add parent category

		temp_dict = {}
		temp_dict['name'] = category.name
		if url:
			temp_dict['url'] = category.get_absolute_url()

		self.crumbs.append(temp_dict)

		return True

	def add_product(self, product, url=True):
		if product.category:
			self.add_category(product.category)
			
		temp_dict = {}
		temp_dict['name'] = product.name
		if url:
			temp_dict['url'] = product.get_absolute_url()

		self.crumbs.append(temp_dict)

		return True