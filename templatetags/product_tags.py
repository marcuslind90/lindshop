from django import template
from lindshop.core.product.models import Product
register = template.Library()

# Return translation of the house type
#@register.filter(name='format_price')
@register.simple_tag(takes_context=True)
def format_price(context, price, args=False):

	if 'request' in context:
		request = context['request']
	else:
		request = None

	if args == "decimals":
		formatted_price = Product.format_price(price, decimals=True, request=request)
	else:
		formatted_price = Product.format_price(price, request=request)
	return formatted_price