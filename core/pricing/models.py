from django.db import models
#from lindshop.core.product.models import Product
#from lindshop.core.subscription.models import Plan

class Currency(models.Model):
	iso_code = models.CharField(max_length=3)
	format = models.CharField(max_length=10, blank=True, null=True)
	default = models.BooleanField(default=False)
	language = models.CharField(max_length=5)
	
	def __unicode__(self):
		return self.iso_code

	@staticmethod
	def get_current_currency(request=None, order=None):
		if request is not None:
			if 'currency' in request.session:
				try:
					currency = Currency.objects.get(iso_code=request.session['currency'])
					return currency
				except Currency.DoesNotExist:
					pass
		elif order is not None:
			return order.cart.currency
			
		currency = Currency.objects.get(default=True)
		return currency

	class Meta:
		app_label = 'pricing'

class Taxrule(models.Model):
	name = models.CharField(max_length=100)
	percentage = models.FloatField()

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'pricing'

class Voucher(models.Model):
	code = models.CharField(max_length=50)
	value = models.IntegerField()
	value_type = models.CharField(max_length=20, choices=(("percentage", "Percentage"), ("value", "Value")))

	def __unicode__(self):
		return self.code

	class Meta:
		app_label = 'pricing'

class Discount(models.Model):
	product = models.ForeignKey('product.Product')
	min_amount = models.IntegerField(default=1)
	value = models.FloatField()
	value_type = models.CharField(max_length=20, choices=(("percentage", "Percentage"), ("value", "Value")))

	def __unicode__(self):
		return self.product.name

	class Meta:
		app_label = 'pricing'	

class Pricing(models.Model):
	product 	= models.ForeignKey('product.Product', null=True, blank=True)
	plan		= models.ForeignKey('subscription.Plan', null=True, blank=True)
	currency 	= models.ForeignKey(Currency)
	taxrule 	= models.ForeignKey(Taxrule)
	price 		= models.FloatField()
	
	def __unicode__(self):
		if self.product is not None:
			return self.product.name
		else:
			return "self.plan.name"

	class Meta:
		app_label = 'pricing'

