from django.conf import settings
from django.utils.module_loading import import_string

payments = {}
for payment in settings.LINDSHOP_PAYMENTS:
	payment_module = import_string(payment)
	payment_class = payment_module()
	payments[payment_class.id] = payment_class