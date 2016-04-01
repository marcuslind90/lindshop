from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone
from django.utils.module_loading import import_string

#from lindshop.core.dashboard import *
from lindshop.core.order.models import Order
from lindshop import config

"""
View that display login form. If user is logged in
then the user will be redirected to the Dashboard index view.
"""
def login_view(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('shop:dashboard:dashboard'))
			else:
				# Return a "This account is distabled" message.
				return HttpResponseRedirect(reverse('shop:dashboard:login')+"?error=disabled.")

		else:
			# Return an invalid login message.
			return HttpResponseRedirect(reverse('shop:dashboard:login')+"?error=failed")


	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('shop:dashboard:dashboard'))
	else:
		return render(request, "lindshop/dashboard/login.html")

"""
Logout view that logout the user and redirect to login page.
"""
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('shop:dashboard:login'))

"""
Index Dashboard view.
"""
def dashboard(request):
	if request.user.is_authenticated():
		orders = Order.objects.all().order_by('-date_created')
		return render(request, "lindshop/dashboard/index.html", {'orders': orders})
	else:
		return HttpResponseRedirect(reverse('shop:dashboard:login')+"?error=noauth")

@login_required
def products(request):
	products = Product.objects.all().order_by('-pk')
	return render(request, "lindshop/dashboard/products.html", {'products': products})

@login_required
def product(request, id_product):
	product = get_object_or_404(Product, pk=id_product)
	return render(request, "lindshop/dashboard/product.html", {'product': product})

@login_required
def categories(request):
	categories = Category.objects.all().order_by('-pk')
	return render(request, "lindshop/dashboard/categories.html", {'categories': categories})

@login_required
def category(request, id_category):
	category = get_object_or_404(Category, pk=id_category)
	return render(request, "lindshop/dashboard/category.html", {'category': category})

"""
Order Dashboard view.
Displays a single order.
"""
@login_required
def order(request, id_order):
	order = get_object_or_404(Order, pk=id_order)
	notifications = order.notification_set.all().order_by("-date_created")
	return render(request, "lindshop/dashboard/order.html", {'order': order, 'notifications': notifications})

@login_required
def subscriptions(request):
	orders = Order.objects.filter(Q(subscription=True) | Q(subscription_enddate__gte=timezone.now()), Q(subscription_status="active") | Q(subscription_status="unpaid"))
	
	small 	= Product.objects.get(pk=3)
	medium 	= Product.objects.get(pk=4)
	large 	= Product.objects.get(pk=5)

	small_count 	= 0
	medium_count 	= 0
	large_count 	= 0

	for order in orders:
		items = order.cart.cartitem_set.all()
		for item in items:
			if item.product == small:
				small_count += 1
			elif item.product == medium:
				medium_count += 1
			elif item.product == large:
				large_count += 1


	return render(request, "lindshop/dashboard/subscriptions.html", {'subscriptions': orders, 'small_count': small_count, 'medium_count': medium_count, 'large_count': large_count})

@login_required
def plans(request):
	return HttpResponse("Loaded")
	
@login_required
def check_payments(request):
	orders = Order.objects.filter(Q(subscription=True) | Q(subscription_enddate__gte=timezone.now()), subscription_status="active")
	subscriptions = []

	# Get the payment class from the configuration and initiate a class.
	payment_module = import_string(config.subscription_payment)
	payment_class = payment_module()

	# Test if each subscription is still a subscriber with the Payment Gateway
	for order in orders:
		# Use the stored payment reference ID and check with the payment gateway
		# if tha reference is still subscribed and paying.
		result = payment_class.checkSubscription(order)
		print "%s == %s" % (order.payment_reference, result)
		if result == 'active': # If active, meaning payments are successful. Do nothing
			pass
		elif result == 'unpaid': # If unpaid, update status to unpaid for the order
			order.subscription_status = 'unpaid'
			order.save()
		elif result == 'canceled': # If canceled, cancel the order.
			order.subscription_status = 'canceled'
			order.save()
		else:
			order.subscription_status = 'canceled'
			order.save()

	return HttpResponse(status=200)

@login_required
def add_notification(request):
	id_order 			= request.POST.get('id_order', None)
	notification_type 	= request.POST.get('notification_type', None)
	note 				= request.POST.get('note', None)

	order = Order.objects.get(pk=id_order)
	note = Notification(order=order, notification_type=notification_type, note=note)
	note.save()

	return HttpResponse(status=200)
