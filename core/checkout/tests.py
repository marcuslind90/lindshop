from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from lindshop.core.cart.models import Cart
from lindshop.core.customer.models import CustomerProfile, Address, Country
from lindshop.core.product.models import Product
from lindshop.core.category.models import Category
from lindshop.core.pricing.models import Currency, Taxrule, Pricing
from lindshop.core.checkout import process
# Create your tests here.
class ViewTests(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.currency = Currency.objects.create(iso_code="SEK", format="%s kr", default=True)
		cls.user = get_user_model().objects.create_user(username="marcuslind90", email="marcuslind90@gmail.com", password="helloworld")
		cls.address = Address.objects.create(user=cls.user)
		cls.cart 	= Cart.objects.create(user=cls.user, currency=cls.currency)
		cls.country = Country.objects.create(name="Thailand", slug="thailand", default=True)

		cls.factory = RequestFactory()
		cls.factory.session = {'id_cart': cls.cart.pk}
		cls.factory.META = {'CSRF_COOKIE_USED': True}
		cls.factory.POST = {
			'first_name': 'Marcus', 
			'last_name': 'Lind', 
			'dog_name': 'Molly', 
			'date_of_birth': '2015-07-15', 
			'email': '', 
			'country': '1', 
			'address': 'Ratchadapisek Soi 20', 
			'city': 'Bangkok', 
			'zipcode': '10310', 
			'phone': '0838275978' 
		}

	def test_validate_checkout(self):
		self.assertEqual(process.validate_checkout(self.factory), True)  # Test if validation can validate a valid request.
		self.factory.POST['address'] = ''  # Set the Address field to something invalid
		self.assertNotEqual(process.validate_checkout(self.factory), True)  # Make sure it's NOT equal to True, meaning it failed.

	def test_get_cart(self):
		self.assertEqual(process.get_cart(self.factory), self.cart)

	def test_add_customer(self):
		self.assertEqual(process.add_customer(self.factory), self.user)  # Make sure the customer object is returned.
		self.assertEqual(process.add_customer(self.factory).first_name, 'Marcus')  # Make sure that the data has been saved.

	def test_add_address(self):
		self.assertEqual(process.add_address(self.factory), self.address)  # Make sure the address object is returned.
		self.assertEqual(process.add_address(self.factory).address, 'Ratchadapisek Soi 20')  # Make sure that the data has been saved.


