from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from lindshop.config import shop_name


class Product(models.Model):
	name = models.CharField(max_length=100)
	short_description = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	attributes = models.ManyToManyField('attribute.Attribute', blank=True)
	slug = models.SlugField(unique=True)
	category = models.ForeignKey('category.Category', null=True)
	active = models.BooleanField(default=False)
	seo_title = models.CharField(max_length=100, blank=True, null=True)
	seo_description = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.name

	@property
	def title(self):
		if self.seo_title:
			return self.seo_title
		else:
			return _('Buy %(product_name)s at %(shop_name)s') % ({'product_name': self.name, 'shop_name': shop_name})


	"""
	Get the featured product image. If multiple images are set
	to featured, only return the first one.

	Return ProductImage object.
	"""
	def get_featured(self):
		images = self.productimage_set.filter(featured=True)
		if len(images) > 0:
			return images[0]

	def get_absolute_url(self):
		return reverse('shop:product', kwargs={'id_product': self.pk, 'slug': self.slug})

	def get_price(self, tax='incl'):
		if tax == 'incl':
			price = self.get_price_incl()
		elif tax == 'excl':
			price = self.get_price_excl()

		return price

	def get_price_excl(self):

		from lindshop.core.pricing.models import Pricing
		try:
			pricing = self.pricing_set.get(product=self, currency__language=get_language())
		except Pricing.DoesNotExist:
			pricing = self.pricing_set.get(product=self, currency__default=True)

		return pricing.price

	def get_price_incl(self):
		from lindshop.core.pricing.models import Pricing
		try:
			pricing = self.pricing_set.get(product=self, currency__language=get_language())
		except Pricing.DoesNotExist:
			pricing = self.pricing_set.get(product=self, currency__default=True)
		#pricing = self.pricing_set.get(product=self)
		tax_multiplier = pricing.taxrule.percentage/100+1
		return pricing.price*tax_multiplier

	def get_vat(self):
		from lindshop.core.pricing.models import Pricing
		try:
			pricing = self.pricing_set.get(product=self, currency__language=get_language())
		except Pricing.DoesNotExist:
			pricing = self.pricing_set.get(product=self, currency__default=True)
		tax_multiplier = pricing.taxrule.percentage/100
		return pricing.price*tax_multiplier

	@staticmethod
	def format_price(price, decimals=False, request=None):
		from lindshop.core.pricing.models import Currency
		if decimals:
			price = "{0:.2f}".format(float(price))
		elif price % 1 == 0:
			price = int(price)
		else:
			price = "{0:.2f}".format(float(price))

		currency = Currency.get_current_currency(request)
		return currency.format % price

	@staticmethod
	def get_popular(amount):
		return Product.objects.all()[:amount]

	class Meta:
		app_label = 'product'

class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to="products")
	alt = models.CharField(max_length=50, blank=True, null=True)
	featured = models.BooleanField(default=False)

	def __unicode__(self):
		return self.product.name

	class Meta:
		app_label = 'product'