from django.core.urlresolvers import reverse, resolve, get_callable
from django.utils import six


def is_crumbed(view):
	return hasattr(get_callable(view), 'crumb_text')


class CrumbedView(object):
	def __init__(self, view, url, args, kwargs):
		view = get_callable(view)
		if (not is_crumbed(view)):
			raise ValueError("The view is not crumbed")
		self._view = view
		self._url = url
		# Theese are exactly those args expected by view, not by url pattern
		self._args = args
		self._kwargs = kwargs

	@property
	def text(self):
		return self._try_call_value(self._view.crumb_text)

	@property
	def _parent_args(self):
		return self._try_call_value(self._view.crumb_p_args)

	@property
	def _parent_kwargs(self):
		return self._try_call_value(self._view.crumb_p_kwargs)

	@property
	def parent_url(self):
		return self._try_call_value(self._view.crumb_parent_url)

	@property
	def parent(self):
		p = getattr(self._view, 'crumb_parent', None)
		if p is None:
			return None
		else:
			v = CrumbedView.get_view_info(p, self.parent_url, self._parent_args, self._parent_kwargs)
			#v = ("", (), {})
			return CrumbedView(p, *v)

	@property
	def url(self):
		return self._url


	def as_dict(self):
		return {'text': self.text, 'url': self.url}

	def _try_call_value(self, val):
		if callable(val):
			return val(*self._args, **self._kwargs)
		else:
			return val


	@staticmethod
	def get_view_info(view, parent_url, pattern_args=[], pattern_kwargs={}):
		'''Resolves pattern args to view args.
		This trick is needed because the view (and provided function) doesn't necessary _expect to get_
		the same arguments as given to url pattern.
		'''
		url = reverse(parent_url, args=pattern_args, kwargs=pattern_kwargs)
		match = resolve(url)
		return (url, match.args, match.kwargs)