import json
import random
import string

from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from lindshop.core.attribute.models import AttributeChoice
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.product.models import Product
from lindshop.core.pricing.models import Voucher, Currency
from lindshop.core.shipping.models import Carrier
from lindshop.core.customer.models import CustomerProfile, Address, Country
from lindshop import config

def ajax_cart(request):
	if request.method == 'POST':
		if request.POST.get('action', None) == "add-product":
			try:
				result = addProduct(request, request.POST.get('id_product', None))
			except Exception as ex:
				print ex

			return result
		elif request.POST.get('action', None) == "add-product-form":
			try:
				result = add_product_from_form(request)
			except Exception as ex:
				print ex

			return result
		elif request.POST.get('action', None) == "update-cart":
			try:
				result = updateCart(request)
			except Exception as ex:
				print ex

			return result
		elif request.POST.get('action', None) == "update-amount":
			try:
				result = updateAmount(request, request.POST.get('id_product', None), request.POST.get('amount', None))
			except Exception as ex:
				print ex

			return result
		elif request.POST.get('action', None) == "remove-product":
			try: 
				result = removeProduct(request, request.POST.get('id_product', None))
			except Exception as ex:
				print ex

			return result
		elif request.POST.get('action', None) == "add-voucher":
			try:
				result = addVoucher(request, request.POST.get('voucher', None))
			except Exception as ex:
				print ex
			return result

		elif request.POST.get('action', None) == "update-carrier":
			try:
				result = updateCarrier(request, request.POST.get('id_carrier', None))
			except Exception as ex:
				print ex

			return result
		elif request.POST.get('action', None) == "update-email":
			try:
				result = updateCustomerEmail(request, request.POST.get('email', None))
			except Exception as ex:
				print ex

			return result
		elif request.POST.get('action', None) == "update-country":
			try:
				result = updateCustomerCountry(request, request.POST.get('id_country', None))
			except Exception as ex:
				print ex

			return result

	return HttpResponse("Nothing Returned")

def get_cart(request):
	"""First see if current user already got a cart.
	If got cart, load it. else create a new one with default settings.
	"""
	if 'id_cart' in request.session:
		cart = Cart.objects.get(pk=request.session['id_cart'])
	else:
		# Get the current currency of the user, or default currency.
		currency = Currency.get_current_currency(request)

		cart = Cart(currency=currency)
		
		# If a Default Carrier exist, then add it to the cart
		# when the user creates his first cart.
		try: 
			carrier = Carrier.objects.get(default=True)
			cart.carrier = carrier
		except Carrier.DoesNotExist:
			pass

		cart.save()

		request.session['id_cart'] = cart.pk

	return cart

def add_product_from_form(request, amount=1):
	"""Add a product from POST form on Product Page.
	Unlike function `addProduct()` this function also adds attributes
	and other product data.
	"""
	cart = get_cart(request)

	attributes = request.POST.getlist('attributes[]', None)
	id_product = request.POST.get('id_product', None)

	attribute_list = []
	attribute_filter = {}

	# Turn a JSON list of attributes into a list (`attribute_list`)
	# of AttributeChoice objects.
	for json_attribute in attributes:
		attribute = json.loads(json_attribute)
		attribute['attribute'] = attribute['attribute'].split('-')[1:][0]  # Remove the "attribute-" part and only keep the real attribute slug.
		
		try:
			attribute_obj = AttributeChoice.objects.get(attribute__slug=attribute['attribute'], slug=attribute['value'])
			attribute_list.append(attribute_obj)
		except AttributeChoice.DoesNotExist:
			pass

	product = Product.objects.get(pk=id_product)

	# If attribute is added. Then check for a CartItem with all those attributes.
	if len(attribute_list) > 0:
		ci = CartItem.objects.filter(cart=cart, product=product, attribute__in=attribute_list).annotate(num_attr=Count('attribute')).filter(num_attr=len(attribute_list))
	# If no attribute is added, check for a CartItem without any attributes at all.
	else:
		ci = CartItem.objects.filter(cart=cart, product=product, attribute__isnull=True)

	# If CartItem that is same to the added product already exist in this cart, 
	# then just update the amount of the already existing cart item.
	if len(ci) > 0:
		ci = ci[0]
		ci.amount += amount
		ci.save()
	# If no CartItem exist, then create a new one. 
	else:
		ci = CartItem(cart=cart, product=product)
		ci.amount = amount
		ci.save()
		ci.attribute.add(*attribute_list)

	return HttpResponse(status=200)

def addProduct(request, id_product, amount=1):

	cart = get_cart(request)

	p = Product.objects.get(pk=id_product)

	try:
		ci = CartItem.objects.get(cart=cart, product=p)
		ci.amount += amount
	except CartItem.DoesNotExist:
		ci = CartItem(cart=cart, product=p)
		ci.amount = amount

	ci.save()

	return HttpResponse("Product Added: %s in Cart #%s" % (p.name, request.session['id_cart']) )

"""
Update the amount of a product in the cart.
This function is used in cart.js ajax call.

Return a text success message.
"""
def updateAmount(request, id_product, amount):
	c = Cart.objects.get(pk=request.session['id_cart'])

	item = c.cartitem_set.get(pk=id_product)
	item.amount = amount
	item.save()

	return HttpResponse("Product Updated, %s is now %s" % (id_product, amount))

def removeProduct(request, id_product):
	cart = Cart.objects.get(pk=request.session['id_cart'])
	#p = Product.objects.get(pk=id_product)
	ci = cart.cartitem_set.get(pk=id_product)
	ci.delete()

	return HttpResponse("Object deleted")

def addVoucher(request, voucher):
	c = Cart.objects.get(pk=request.session['id_cart'])

	try:
		voucher = Voucher.objects.get(code=voucher)
		c.voucher = voucher
		c.save()

	except Voucher.DoesNotExist:
		return JsonResponse({
			'error': _("We could not find the voucher that you added.")
			})

	return JsonResponse({
			'success': _('A voucher has been added to your cart.')
			})

def updateCarrier(request, id_carrier):
	c = Cart.objects.get(pk=request.session['id_cart'])
	carrier = Carrier.objects.get(pk=id_carrier)
	c.carrier = carrier
	c.save()

	return HttpResponse("Carrier Updated Successfully.")

def updateCustomerEmail(request, email):
	cart = Cart.objects.get(pk=request.session['id_cart'])
	if cart.user:
		cart.user.email = email
		cart.user.save()
	else:
		#customer = Customer(email=email)
		#customer.save()
		password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
		user = get_user_model().objects.create_user(username=email, email=email, password=password)
		cart.user = user
		cart.save()

	return HttpResponse("Updated Email")

def updateCustomerCountry(request, id_country):
	cart = Cart.objects.get(pk=request.session['id_cart'])
	country = Country.objects.get(pk=id_country)
	# If customer exist, check if address exists.
	# If address exists, set country. If not, create a new address.
	if cart.user:
		if cart.user.user_address.all()[0]:
			address = cart.user.user_address.all()[0]
			address.country = country
			address.save()
		else:
			address = Address(user=cart.user, country=country)
			address.save()
	# If no customer exists yet, create a customer, save it, connect to cart
	# and add a address to the customer with the country set.
	else:
		return HttpResponse("Can't Update Country: No customer exist yet.")

	return HttpResponse("Updated Country to: %s" % country.name)

def updateCart(request):
	if 'id_cart' in request.session:
		cart = Cart.objects.get(pk=request.session['id_cart'])
		items = cart.cartitem_set.all()
		html = ""
		for item in items:
			html = "%s %s" % (html, render_to_string('lindshop/cart-dropdown-item.html', {'item': item, 'cart': cart, 'config': config}))
		response = {
			'html': html, 
			'amount': len(items), 
			'total': cart.get_total(formatted=True), 
			'total_decimals': cart.get_total(formatted=True, decimals=True), 
			'total_vat': cart.get_total_vat(formatted=True, decimals=True), 
			'total_discount': cart.get_total_discount(formatted=True, decimals=True), 
			'total_to_pay': cart.get_to_pay(formatted=True, decimals=True), 
			'total_shipping': cart.get_shipping(formatted=True, decimals=True), 
		}

		if cart.user is not None:
			response['id_address'] = cart.user.user_address.all()[0].pk

		return JsonResponse(response)