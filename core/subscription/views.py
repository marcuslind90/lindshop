import json
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_GET
from django.utils.module_loading import import_string

from lindshop.core.product.models import Product
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.customer.models import CustomerProfile, Address
from lindshop.core.cart.views import addProduct
from lindshop.core.shipping.models import Carrier
from lindshop.core.subscription.models import Plan

from lindshop.core.attribute.models import Attribute
from lindshop import config

@require_GET
def subscription_cancel(request):
	uid = request.GET.get('u', None)
	key = request.GET.get('key', None)

	try:
		customer = Customer.objects.get(pk=uid, key=key)
	except Customer.DoesNotExist:
		return HttpResponse(status=404)


	orders = customer.order_set.filter(subscription_status="active")
	if len(orders) > 0:

		# Get the payment class from the configuration and initiate a class.
		payment_module = import_string(config.subscription_payment)
		payment_class = payment_module()

		for order in orders:
			if payment_class.unsubscribe(order.payment_reference, order.payment_id):
				order.subscription_status = "canceled"
				order.save()

		# Send Email Confirmation about the cancelation.
		subject = _('TailBay Cancel Subscription Confirmation')
		logo = config.shop_logo
		shop_name = config.shop_name
		# Load the Email Template and save the HTML as a string.
		msg_html = render_to_string('shop/mail/subscription-cancel-confirmation.html', 
			{
				'subject': subject, 
				'logo': logo, 
				'shop_name': shop_name
			}
		)

		# Load the Text message. This is send as a backup together with the HTML message
		# for the users that can not see HTML emails.
		msg_text = render_to_string('shop/mail/subscription-cancel-confirmation.txt', 
			{}
		)

		# Django's build in send_mail function. Settings set in settings.py
		send_mail(
			subject=subject, 
			message=msg_text, 
			from_email="info@tailbay.com", 
			recipient_list=[customer.email], 
			html_message=msg_html
		)


		return HttpResponseRedirect(reverse('shop:subscription-change')+'?success=unsubscribed')
	else:
		return HttpResponse(status=404) # No orders active.

def subscription_change(request):
	if request.method == "POST":
		email = request.POST.get('cancel_email', None)

		try:
			customer = Customer.objects.get(email=email)
		# If customer does not exist, return "email does not exist" error
		except Customer.DoesNotExist:
			return HttpResponseRedirect(reverse('shop:subscription-change')+'?error=email_nofound')

		subject = _('TailBay Cancel Subscription')
		logo = config.shop_logo
		shop_name = config.shop_name
		cta_link = request.build_absolute_uri(reverse('shop:subscription-cancel')+"?u=%s&key=%s" % (customer.pk, customer.key))
		# Load the Email Template and save the HTML as a string.
		msg_html = render_to_string('shop/mail/subscription-cancel.html', 
			{
				'subject': subject, 
				'logo': logo, 
				'shop_name': shop_name, 
				'cta_link': cta_link, 
				'cta_text': _('Cancel Subscription')
			}
		)

		# Load the Text message. This is send as a backup together with the HTML message
		# for the users that can not see HTML emails.
		msg_text = render_to_string('shop/mail/subscription-cancel.txt', 
			{}
		)

		# Django's build in send_mail function. Settings set in settings.py
		send_mail(
			subject=subject, 
			message=msg_text, 
			from_email="info@tailbay.com", 
			recipient_list=[customer.email], 
			html_message=msg_html
		)

		return HttpResponseRedirect(reverse('shop:subscription-change')+'?success=email_send')

	return render(request, "lindshop/subscription-change.html")

def add_subscription(request, attributes=None):
	if request.method == "POST":
		plan = request.POST.get('plan', None)
		pet_size = request.POST.get('pet_size', None)
		upgrade = request.POST.get('upgrade', None)

		email = request.POST.get('email', None)

		# If user already have a cart when we try to add a product.
		# Remove the session (remove connection between user and cart)
		# to start on new cart.
		if 'id_cart' in request.session:
			request.session['id_cart'] = None
			request.session.pop('id_cart', None)

		# Get amount of months for the plan
		try:
			amount = int(plan.split('-')[0])
		except Exception as ex:
			pass # Return 404

		if upgrade == 'upgrade':
			try:
				plan_object = Plan.objects.get(slug=plan, premium=True)
			except Plan.DoesNotExist:
				pass # Return error
		else:
			try:
				plan_object = Plan.objects.get(slug=plan, premium=False)
			except Plan.DoesNotExist:
				pass # Return error

		# Create a new customer
		try: 
			customer = Customer.objects.get(email=email)
			address = customer.user_address.all()[0]
		except Customer.DoesNotExist:
			customer = Customer(email=email)
			customer.save()

			# Create a new address
			address = Address(customer=customer)
			address.save()



		# Create a new cart
		cart = Cart(customer=customer)

		# Add default shipping to cart
		# If a Default Carrier exist, then add it to the cart
		# when the user creates his first cart.
		try: 
			carrier = Carrier.objects.get(default=True)
			cart.carrier = carrier
		except Carrier.DoesNotExist:
			pass

		cart.save()
		request.session['id_cart'] = cart.pk

		# Add item to Cart
		ci = CartItem(cart=cart, plan=plan_object)
		ci.amount = amount
		ci.save()

		# If attributes are set, then also add the attributes
		# to this cartitem.
		if attributes:
			for k, v in attributes.iteritems():
				attribute = Attribute.objects.get(slug=k)
				choice = attribute.attributechoice_set.get(slug=v)

				ci.attribute.add(choice)
				ci.save()

		# Return True on success
		return True
	else:
		pass # Return 404