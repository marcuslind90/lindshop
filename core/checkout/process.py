import random
import string

from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from lindshop.core.cart.models import Cart
from lindshop.core.customer.models import Address, Country
from lindshop.core.order.models import Order, CustomField, CustomFieldValue
from lindshop.core.payment.utils import payments

def validate_checkout(request):
	"""Validate the inputs of the checkout form.
	Return True if validation success.
	"""
	# Get personal data
	first_name = request.POST.get('first_name', None)
	last_name = request.POST.get('last_name', None)
	dog_name = request.POST.get('dog_name', None)
	date_of_birth = request.POST.get('date_of_birth', None)
	email = request.POST.get('email', None)

	# Get Address Data
	country = request.POST.get('country', None)
	address = request.POST.get('address', None)
	city 	= request.POST.get('city', None)
	zipcode = request.POST.get('zipcode', None)
	phone 	= request.POST.get('phone', None)

	status = True
	errors = []

	# Check if any fields are empty
	if first_name is None or len(first_name) < 1:
		status = False
		errors.append(_('First name field is empty.'))

	if last_name is None or len(last_name) < 1:
		status = False
		errors.append(_('Last name field is empty.'))

	if email is None or len(email) < 1:
		if 'id_cart' in request.session:
			cart = Cart.objects.get(pk=request.session['id_cart'])
			if cart.user and cart.user.email is None:
				status = False
				errors.append(_('Email field is empty.'))
			else:
				pass
		else:
			status = False
			errors.append(_('Email field is empty.'))

	if country is None or len(country) < 1:
		status = False
		errors.append(_('Country field is empty.'))

	if address is None or len(address) < 1:
		status = False
		errors.append(_('Address field is empty.'))

	if city is None or len(city) < 1:
		status = False
		errors.append(_('City field is empty.'))

	if zipcode is None or len(zipcode) < 1:
		status = False
		errors.append(_('Zipcode field is empty.'))

	if phone is None or len(phone) < 1:
		status = False
		errors.append(_('Phone field is empty.'))

	if 'id_cart' not in request.session:
		status = False
		errors.append(_('No cart exist for this session.'))

	if status:
		return True
	else:
		return errors

def get_cart(request):
	return Cart.objects.get(pk=request.session['id_cart'])

def get_plan(request):
	"""Get the Subscription Plan of the cart.
	Return `Plan` object on success. Return False on fail.
	"""
	cart = Cart.objects.get(pk=request.session['id_cart'])
	products = cart.cartitem_set.filter(plan__isnull=False)
	plan = None  # Set plan to None by default
	if len(products) > 0:
			plan = products[0].plan

	return plan

def add_customer(request):
	"""Add data to the customer object.
	Return customer object.
	"""
	# Get personal data
	first_name = request.POST.get('first_name', None)
	last_name = request.POST.get('last_name', None)
	dog_name = request.POST.get('dog_name', None)
	date_of_birth = request.POST.get('date_of_birth', None)
	email = request.POST.get('email', None)
	phone = request.POST.get('phone', None)

	cart = Cart.objects.get(pk=request.session['id_cart'])
	if cart.user is None:
		try:
			user = get_user_model().objects.get(username=email)
		except get_user_model().DoesNotExist:
			password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
			user = get_user_model().objects.create_user(
				username=email, 
				first_name=first_name, 
				last_name=last_name,
				email=email, 
				password=password
			)
		cart.user = user
		cart.save()
	else:
		cart.user.first_name = first_name
		cart.user.last_name = last_name
		cart.user.email = email
		cart.user.save()

	return cart.user

def add_address(request):
	"""Add data to the address object.
	Return address object.
	"""
	country = request.POST.get('country', None)
	address = request.POST.get('address', None)
	city = request.POST.get('city', None)
	zipcode = request.POST.get('zipcode', None)

	cart = Cart.objects.get(pk=request.session['id_cart'])

	# Get country object of country.
	country_obj = Country.objects.get(pk=country)

	# If user already have an address.
	if len(cart.user.user_address.all()) > 0:
		customer_address = cart.user.user_address.all()[0]
		customer_address.country = country_obj
		customer_address.address = address
		customer_address.city = city
		customer_address.zipcode = zipcode
		customer_address.save()
	# Else create a new address
	else:
		customer_address = Address(
			user=cart.user, 
			country=country_obj, 
			address=address, 
			city=city, 
			zipcode=zipcode, 
		)
		customer_address.save()

	return customer_address

def add_custom_fields(request, order):
	custom_fields = CustomField.objects.all()
	for field in custom_fields:
		value = request.POST.get(field.slug, None)
		if value is not None:
			value = CustomFieldValue.objects.create(
				custom_field = field, 
				order = order, 
				value = value
			)
		elif field.mandatory: # If field is not part of the request, but its mandatory. Raise an error.
			raise ValueError('Mandatory field "%s" is not set.' % field.slug)

	return True

def add_order(cart, customer, **kwargs):
	"""Add order data to the `Order` object.
	Return `Order` object.
	"""
	order = Order(
		cart=cart, 
		user=cart.user, 
		payment_id=id_payment_subscription, 
		payment_reference=id_payment_customer
	)

	if 'payment_id' in kwargs:
		order.payment_id = kwargs['payment_id']

	if 'payment_reference' in kwargs:
		order.payment_reference = kwargs['payment_reference']

	if plan is not None:
		order.subscription 			= True
		order.subscription_status 	= result['status']
		order.subscription_plan 	= plan
		order.subscription_enddate	= plan.get_expire()

	order.save()

def do_transaction(request, order):
	"""Get the payment option of the order, and complete the transaction.
	Return a dictionary of data on success. Return False on failed.
	"""
	payment = payments[order.payment_option]

	if order.subscription:
		return payment.do_subscription_transaction(request, order)
	else:
		return payment.do_transaction(request, order)
