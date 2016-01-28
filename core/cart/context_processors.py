from lindshop.core.cart.models import Cart
from django.conf import settings
from lindshop import config
"""
This is a Template Context Processor that include
all Cart Items on every template, to make the cart
available globally on each page of the website.

Call {{cart_items}} in template.
"""
def template_processor(request):
	try:
		base_template = config.shop_base_template
	except:
		base_template = "shop/base.html"

	return {'base_template': base_template}

def config_processor(request):
	return {'config': config}

def cart_processor(request):
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

	return {'cart': cart, 'cart_items': items}