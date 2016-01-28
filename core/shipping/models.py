from django.db import models
#from lindshop.core.pricing.models import Taxrule, Currency
#from lindshop.core.customer.models import Country

class Carrier(models.Model):
	name = models.CharField(max_length=50)
	delivery_text = models.CharField(max_length=100)
	logo = models.ImageField(upload_to="carriers", null=True, blank=True)
	default = models.BooleanField(default=True)
	countries = models.ManyToManyField('customer.Country')
	
	def get_total(self):
		price = self.carrierpricing_set.get(carrier=self)
		return price.get_total()

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'shipping'

class CarrierPricing(models.Model):
	carrier = models.ForeignKey(Carrier)
	currency = models.ForeignKey('pricing.Currency')
	taxrule = models.ForeignKey('pricing.Taxrule')
	price = models.FloatField()

	def __unicode__(self):
		return self.carrier.name
		
	def get_total(self):
		return self.price*(self.taxrule.percentage/100+1)

	class Meta:
		app_label = 'shipping'