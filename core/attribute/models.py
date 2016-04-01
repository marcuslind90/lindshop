from django.db import models
from lindshop.core.product.models import Product

class Attribute(models.Model):
	name = models.CharField(max_length=100)
	text_input = models.BooleanField(default=False)
	slug = models.SlugField()
	product = models.ForeignKey(Product)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'attribute'


class AttributeChoice(models.Model):
	attribute 	= models.ForeignKey(Attribute)
	value		= models.CharField(max_length=100)
	slug		= models.SlugField(blank=True)

	def __unicode__(self):
		return "%s, %s" % (self.attribute.name, self.value)

	class Meta:
		app_label = 'attribute'