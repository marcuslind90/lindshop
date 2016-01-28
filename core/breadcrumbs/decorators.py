def crumb(text, parent=None, parent_url=None, parent_args=[], parent_kwargs={}):

	def _crumbed(view):
		view.crumb_text = text
		view.crumb_parent = parent
		view.crumb_parent_url = parent_url
		view.crumb_p_args = parent_args
		view.crumb_p_kwargs = parent_kwargs
		return view

	return _crumbed