from django.db import models
#from lindshop.core.product.models import Product

class Warehouse(models.Model):
	name = models.CharField(max_length=100, default="Default", unique=True)
	address = models.CharField(max_length=255)
	country = models.ForeignKey('customer.Country')
	default = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'stock'

class Stock(models.Model):
	product = models.ForeignKey('product.Product')
	warehouse = models.ForeignKey(Warehouse)
	stock = models.IntegerField()
	shelf = models.CharField(max_length=50, blank=True, null=True)

	def __unicode__(self):
		return self.product.name
	
	class Meta:
		app_label = 'stock'

