from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.utils.translation import get_language
#from lindshop.core.attribute.models import Attribute

class Plan(models.Model):
	name 	= models.CharField(max_length=100)
	months 	= models.IntegerField(default=1)
	image	= models.ImageField(upload_to="plans", null=True, blank=True)
	premium	= models.BooleanField(default=False)
	attributes = models.ManyToManyField('attribute.Attribute')
	slug 	= models.SlugField()

	def __unicode__(self):
		return self.name

	"""
	Get the date that the subscription will expire after a start or renewal. 
	"""
	def get_expire(self):
		return date.today() + relativedelta(months=+self.months)

	def get_price(self, tax='incl'):
		if tax == 'incl':
			price = self.get_price_incl()
		elif tax == 'excl':
			price = self.get_price_excl()

		return price

	def get_price_excl(self):
		from lindshop.core.pricing.models import Pricing
		try:
			pricing = self.pricing_set.get(plan=self, currency__language=get_language())
		except Pricing.DoesNotExist:
			pricing = self.pricing_set.get(plan=self, currency__default=True)

		return pricing.price

	def get_price_incl(self):
		from lindshop.core.pricing.models import Pricing
		try:
			pricing = self.pricing_set.get(plan=self, currency__language=get_language())
		except Pricing.DoesNotExist:
			pricing = self.pricing_set.get(plan=self, currency__default=True)

		tax_multiplier = pricing.taxrule.percentage/100+1
		return pricing.price*tax_multiplier

	def get_monthly_price(self):
		return self.get_price_incl()/self.months


	class Meta:
		app_label = 'subscription'