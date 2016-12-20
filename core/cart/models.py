from django.db import models
from django.conf import settings
from lindshop.core.product.models import Product

class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	voucher = models.ForeignKey('pricing.Voucher', blank=True, null=True)
	carrier = models.ForeignKey('shipping.Carrier', blank=True, null=True)
	currency = models.ForeignKey('pricing.Currency')

	def __unicode__(self):
		return "#%s" % (self.id)

	def get_total(self, formatted=False, decimals=False):
		items = self.cartitem_set.all()
		total = 0
		for item in items:
			total += item.get_total()

		if formatted:
			if decimals:
				total = Product.format_price(total, decimals=True)
			else:
				total = Product.format_price(total)

		return total

	def get_total_vat(self, formatted=False, decimals=False):
		items = self.cartitem_set.all()
		total = 0
		for item in items:
			total += item.product.get_vat()*item.amount

		if formatted:
			if decimals:
				total = Product.format_price(total, decimals=True)
			else:
				total = Product.format_price(total)

		return total

	def get_total_discount(self, formatted=False, decimals=False):
		total = 0
		price = self.get_total()

		if self.voucher is not None:
			if self.voucher.value_type == 'percentage':
				total = price*self.voucher.value/100
			elif self.voucher.value_type == 'value':
				if self.voucher.value > price:
					total = price
				else:
					total = self.voucher.value

			if formatted:
				if decimals:
					total = Product.format_price(total, decimals=True)
				else:
					total = Product.format_price(total)

		return total

	def get_shipping(self, formatted=False, decimals=False):
		total = 0
		if self.carrier:
			total = self.carrier.get_total()

		if formatted:
			if decimals:
				total = Product.format_price(total, decimals=True)
			else:
				total = Product.format_price(total)

		return total

	def get_to_pay(self, formatted=False, decimals=False):
		total = 0
		total += self.get_total()
		total -= self.get_total_discount()
		total += self.get_shipping()

		if formatted:
			if decimals:
				total = Product.format_price(total, decimals=True)
			else:
				total = Product.format_price(total)

		return total


	class Meta:
		app_label = 'cart'

class CartItem(models.Model):
	cart 	= models.ForeignKey('cart.Cart')
	product = models.ForeignKey('product.Product', null=True, blank=True)
	amount 	= models.IntegerField(default=1)
	attribute = models.ManyToManyField('attribute.AttributeChoice')

	def __init__(self, *args, **kwargs):
		total = 100
		super(CartItem, self).__init__(*args, **kwargs)
		total = 10

	@property
	def name(self):
		return self.product.name
			
	def get_product_price(self):
		return self.get_price(self.product, self.amount)
		
	@staticmethod
	def get_price(product, amount):
		try:
			discount = product.discount_set.filter(min_amount__lte=amount).order_by('-min_amount')
		except:
			discount = []
		if len(discount) > 0:
			price = int(product.get_price('incl')*((100-float(discount[0].value))/100))
		else:
			price = product.get_price('incl')
		return price

	def get_total(self):
			return self.amount*self.get_price(self.product, self.amount)		

	class Meta:
		app_label = 'cart'