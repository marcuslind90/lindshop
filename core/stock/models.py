from django.db import models
#from lindshop.core.product.models import Product

class Warehouse(models.Model):
	name = models.CharField(max_length=100, default="Default", unique=True)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'stock'

class Stock(models.Model):
	product = models.ForeignKey('product.Product')
	warehouse = models.ForeignKey(Warehouse)
	stock = models.IntegerField()

	def __unicode__(self):
		return self.product.name
	
	class Meta:
		app_label = 'stock'

