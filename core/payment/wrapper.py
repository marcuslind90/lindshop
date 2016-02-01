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

class SubscriptionPaymentModule(PaymentModule):
	def __init__(self, *args, **kwargs):
		super(SubscriptionPaymentModule, self).__init__(self, *args, **kwargs)
		self.id 	= 'subscription_payment_module'
		self.name 	= 'Subscription Payment Module'

	"""
	Subscribe the user to a Subscription Plan
	"""
	def subscribe(self, *args):
		return {
			'id_customer': self.id, 
			'id_subscription': self.id, 
			'status': 'active'
		}

	"""
	Create/Get the Plan ID of the subscription service.
	"""
	def create_id(self, *args):
		pass

	"""
	Unsubscribe a user from a Subscription Plan
	"""
	def unsubscribe(self, *args):
		pass

	"""
	Check if a user has an active subscription
	"""
	def checkSubscription(self, *args):
		pass
