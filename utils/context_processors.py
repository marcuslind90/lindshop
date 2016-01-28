from lindshop.core.cart.models import Cart
from lindshop.core.category.models import Category
from django.conf import settings
from lindshop import config
"""
This is a Template Context Processor that include
all Cart Items on every template, to make the cart
available globally on each page of the website.

Call {{cart_items}} in template.
"""

def shop_processor(request):
	context = {}
	context = get_cart(context, request)
	context = get_config(context)
	context = get_categories(context)

	return context

def get_cart(context, request):
	if 'id_cart' in request.session:
		try:
			cart = Cart.objects.get(pk=request.session['id_cart'])
			items = cart.cartitem_set.all()
		except Cart.DoesNotExist:
			items = None
			cart = None
	else:
		items = None
		cart = None

	context['cart'] = cart
	context['cart_items'] = items
	return context

def get_config(context):
	context['config'] = config
	return context

def get_categories(context):
	categories = Category.objects.filter(parent=None).order_by(config.category_order_by)
	context['categories'] = categories
	return context