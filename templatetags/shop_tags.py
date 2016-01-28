from django import template
from django.utils.translation import get_language
from lindshop import config
from lindshop.core.menu.models import Menu

register = template.Library()

# Return translation of the house type
@register.filter(name='strip_lang')
def strip_lang(value): # Only one argument.
	lang = get_language()
	return '/%s' % value.replace('/%s/' % lang, '')	

@register.filter(name='get_column')
def get_column(value, arg): # Only one argument.
	column = 12/int(value)
	return "col-%s-%s" % (arg, column)

@register.filter(name="order_category")
def order_category(value):
	"""Takes a QuerySet of `Category` and sort it to 
	either the default sorting or the sorting choosen
	by the user and stored in its session.
	"""
	return value.order_by(config.category_order_by)

@register.inclusion_tag('menu/menu.html')
def menu(menu_slug):
	try:
		menu = Menu.objects.get(slug=menu_slug)
	except Menu.DoesNotExist:
		return {}

	menu_items = sorted(menu.items.all(), key=lambda t: t.label)  # Sort by @property label. (A-Z sorting)

	return {'menu': menu, 'menu_items': menu_items}
