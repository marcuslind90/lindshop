from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.conf import settings
from django.views.decorators.http import require_POST

from lindshop.core.shipping.models import Carrier
from lindshop.core.customer.models import Country
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.order.models import Order, CustomField
from lindshop.core.payment.utils import payments
from lindshop.core.checkout import process

# Create your views here.
def checkout(request, errors=None):
	"""View to display the standard Checkout page with forms, payment
	and extra fields.
	"""
	if 'id_cart' not in request.session:
		return HttpResponseRedirect(reverse('shop:index'))

	countries = Country.objects.all()
	carriers = list_carriers(request)
	custom_fields = CustomField.objects.all()

	#carriers = Carrier.objects.all().order_by('-default')
	return render(request, 'checkout.html', {
		'carriers': carriers, 
		'countries': countries, 
		'errors': errors, 
		'payments': payments, 
		'custom_fields': custom_fields
	})

def ajax_checkout(request):
	"""View that handles AJAX calls on the Checkout Page.
	For example, when a user change country it should load the carriers
	available in that country. This requires an AJAX call.
	"""
	try:
		if request.method == 'POST':
			if request.POST.get('action', None) == "list-carriers":
				result = list_carriers(request, True) # True, to return a HTML string to give back to the JS.
				return result

		return HttpResponse("Nothing Returned")
	except Exception as ex:
		print ex.message

def list_carriers(request, html=False):
	"""Function that returns the carriers available depending on what
	country the user has selected.
	html=True returns a HTML string.
	html=False returns a list of carrier objects.
	"""
	default_country = None
	try:
		if 'id_cart' in request.session:
			cart = Cart.objects.get(pk=request.session['id_cart'])
			if cart.user and cart.user.user_address.all()[0].country:
				default_country = cart.user.user_address.all()[0].country
	except Exception as ex:
		print ex.message

	if default_country is None:
		# If default country exists for the shop. Then only get carriers for that country.
		try:
			default_country = Country.objects.get(default=True)
		except Country.DoesNotExist:
			default_country = Country.objects.get(pk=1) # Set the first country as default if no default country is set.

	carriers = Carrier.objects.filter(countries=default_country).order_by('-default')

	# If html args is True, then return a HTML string of the carrier list.
	if html:
		return HttpResponse(render_to_string('checkout-carrier-list.html', {'carriers': carriers, 'cart': cart}))
	# Else just return a list of objects.
	else:
		return carriers

@require_POST
def process_checkout(request):
	"""View to handle the Form Submit of the Checkout.
	This is where all data from the Checkout is processed and
	used to create an Order.
	"""
	# Validate Data, if failed, return checkout view again and display errors.
	errors = process.validate_checkout(request)
	if errors is not True:
		return checkout(request, errors)

	# Get the cart that is being checked out
	cart = process.get_cart(request)

	# Add User Data
	user = process.add_customer(request)

	# Add Address Data
	address = process.add_address(request)

	# Add Order Data
	order = Order(
		cart=cart, 
		user=user, 
		payment_option=request.POST.get('payment-option', None)
	)

	# Try uncommenting this line, to see if we can still process the transaction witout a saved order in the database.
	order.save()  # Save the order before we do the transaction, in case of error.


	# Add Custom Fields Data
	custom_fields = process.add_custom_fields(request, order)

	# Complete Transaction
	transaction_result = process.do_transaction(request, order)

	if 'error' not in transaction_result:
		print "Transaction Results are: %s" % transaction_result
		order.payment_status = transaction_result['payment_status']
		order.save()

		# Send confirmation email to the customer.
		try:
			order.send_confirmation()
		except Exception as ex:
			print "Error sending confirmation: %s" % ex.message

		# Callback to the payment module used when order is saved.
		payments[order.payment_option].order_success(order)

		#  Reset Cart
		del request.session['id_cart']
		return HttpResponseRedirect(reverse('shop:thank_you'))

	else:
		return HttpResponseRedirect(reverse('shop:checkout')+"?error=%s" % transaction_result['error'])

def thank_you(request):
	return render(request, "lindshop/thank-you.html")