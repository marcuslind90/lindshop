from django import template
from django.utils.translation import get_language
from lindshop import config
from lindshop.core.menu.models import Menu
from lindshop.core.category.models import Category
from lindshop.core.slideshow.models import Slideshow

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

@register.simple_tag
def get_menu(id_menu):
	try:
		menu = Menu.objects.get(pk=id_menu)
	except Menu.DoesNotExist:
		return
		
	menuitems = menu.menuitem_set.all()

	for item in menuitems:
		# If no custom label is set...
		if item.label == '':
			# ... check type and decide how to get label
			if item.item_type == 'category':
				category = Category.objects.get(pk=item.object_id)
				item.label = category.name

		# If no custom URL is set...
		if item.url == '':
			# ... check type and decide ho to get url
			if item.item_type == 'category':
				category = Category.objects.get(pk=item.object_id)
				item.url = category.get_absolute_url


	return menuitems

@register.simple_tag
def get_slideshow(id_slideshow):
	try:
		slideshow = Slideshow.objects.get(pk=id_slideshow)
	except Slideshow.DoesNotExist:
		return
		
	slides = slideshow.slide_set.all()
	return slides