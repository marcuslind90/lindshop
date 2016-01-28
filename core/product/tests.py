from django.test import TestCase, RequestFactory
from django.http import HttpResponse

from lindshop.core.product.models import Product, ProductImage
from lindshop.core.category.models import Category
from lindshop.core.pricing.models import Currency, Taxrule, Pricing

# Create your tests here.
class ProductTests(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.currency 	= Currency.objects.create(name="SEK", format="%s kr", default=True)
		cls.taxrule 	= Taxrule.objects.create(name="25 Standard", percentage=25)
		cls.category 	= Category.objects.create(name="Men Shirts", slug="men-shirts")
		cls.product 	= Product.objects.create(name="Green T-shirt", slug="green-tshirt", active=True)
		cls.pricing 	= Pricing.objects.create(product=cls.product, currency=cls.currency, taxrule=cls.taxrule, price=79.2)

		cls.factory = RequestFactory()

	def test_get_price(self):
		# Test get price incl.
		price = self.product.get_price_excl()
		self.assertEqual(price, 79.2)
		# Test get price excl
		price = self.product.get_price_incl()
		self.assertEqual(price, 99)

	def test_get_vat(self):
		vat = self.product.get_vat()
		self.assertEqual(vat, 19.8)

	def test_format_price(self):
		price = Product.format_price(99)
		self.assertEqual(price, "99 kr")