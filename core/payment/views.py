import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from lindshop.core.order.models import Order
from lindshop.core.payment import payments

"""
If a payment fails or any other interesting event
occur, the payment gateway will send us a event in json.

Here we recieve the JSON and update the order if needed.
"""
@require_POST
@csrf_exempt
def payment_webhook(request):
	event_json = json.loads(request.body)
	if 'type' in event_json:
		if event_json['type'] == 'invoice.payment_failed':
			id_subscription = event_json['data']['subscription']
			pass
		# If a payment is successful, then update the `subscription_enddate` of the order
		# with a date in the future based on `plan.get_expire()`.
		elif event_json['type'] == 'invoice.payment_succeeded':
			id_subscription = event_json['data']['subscription']
			try:
				order = Order.objects.get(payment_id=id_subscription)
				order.subscription_enddate = order.plan.get_expire()
				order.save()
			except Order.DoesNotExist:
				pass

	return HttpResponse(status=200)

def get_form(request):
	id_payment = request.POST.get('id_payment', None)

	if id_payment:
		try:
			html = payments[id_payment].get_form()
		except Exception as ex:
			print ex.message
	
	return HttpResponse(html)