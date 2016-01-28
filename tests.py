from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from lindshop.core.cart.models import Cart
from lindshop.core.customer.models import Country
from lindshop.core.product.models import Product
from lindshop.core.category.models import Category
from lindshop.core.pricing.models import Currency, Taxrule, Pricing
from lindshop.core.checkout.views import checkout
# Create your tests here.
class ViewTests(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.cart 	= Cart.objects.create()
		cls.country = Country.objects.create(name="Thailand", slug="thailand", default=True)
		cls.currency = Currency.objects.create(name="SEK", format="%s kr", default=True)
		cls.taxrule = Taxrule.objects.create(name="25 Standard", percentage=25)
		cls.category = Category.objects.create(name="Men Shirts", slug="men-shirts")
		cls.product1 = Product.objects.create(name="Green T-shirt", slug="green-tshirt", category=cls.category, active=True)
		cls.product2 = Product.objects.create(name="Red T-shirt", slug="red-tshirt", category=cls.category, active=True)
		cls.pricing1 = Pricing.objects.create(product=cls.product1, currency=cls.currency, taxrule=cls.taxrule, price=79.2)
		cls.pricing2 = Pricing.objects.create(product=cls.product2, currency=cls.currency, taxrule=cls.taxrule, price=79.2)

		cls.factory = RequestFactory()
		cls.factory.session = {'id_cart': cls.cart.pk}
		cls.factory.META = {'CSRF_COOKIE_USED': True}

	def test_index_view(self):
		response = self.client.get(reverse('shop:index'))
		self.assertEqual(response.status_code, 200)

	def test_checkout_view(self):
		response = checkout(self.factory)
		self.assertEqual(response.status_code, 200)

	def test_thankyou_view(self):
		response = self.client.get(reverse('shop:thank_you'))
		self.assertEqual(response.status_code, 200)

	def test_terms_view(self):
		response = self.client.get(reverse('shop:terms'))
		self.assertEqual(response.status_code, 200)

	def test_contact_view(self):
		response = self.client.get(reverse('shop:contact'))
		self.assertEqual(response.status_code, 200)

	def test_faq_view(self):
		response = self.client.get(reverse('shop:faq'))
		self.assertEqual(response.status_code, 200)

	def test_product_view(self):
		response = self.client.get(reverse('shop:product', kwargs={'id_product': self.product1.pk, 'slug': self.product1.slug}))
		self.assertEqual(response.status_code, 200)

	def test_subscriptionchange_view(self):
		response = self.client.get(reverse('shop:subscription-change'))
		self.assertEqual(response.status_code, 200)
