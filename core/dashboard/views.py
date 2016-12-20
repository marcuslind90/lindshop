from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone
from django.utils.module_loading import import_string
from django.conf import settings

#from lindshop.core.dashboard import *
from lindshop.core.order.models import Order
from lindshop import config

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

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('shop:dashboard:login'))

def dashboard(request):
	if request.user.is_authenticated():
		orders = Order.objects.all().order_by('-date_created')
		return render(request, "lindshop/dashboard/index.html", {'orders': orders, 'STATIC_URL': settings.STATIC_URL})
	else:
		return HttpResponseRedirect(reverse('shop:dashboard:login')+"?error=noauth")

@login_required
def add_notification(request):
	id_order 			= request.POST.get('id_order', None)
	notification_type 	= request.POST.get('notification_type', None)
	note 				= request.POST.get('note', None)

	order = Order.objects.get(pk=id_order)
	note = Notification(order=order, notification_type=notification_type, note=note)
	note.save()

	return HttpResponse(status=200)
