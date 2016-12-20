from django.template.loader import render_to_string
class PaymentModule(object):
	def __init__(self, *args, **kwargs):
		self.id 	= 'payment_module'
		self.name 	= 'Payment Module'
		self.label 	= 'Credit Card'
		self.js = []

	def get_form(self):
		html = render_to_string('lindshop/payment-form.html')
		return html

	def do_transaction(self, request, order):
		result = {
				'status': 'pending', 
				'payment_status': 'paid'
			}
		return result

	"""
	Function run when an order is successfully saved.
	"""
	def order_success(self, order):
		return None