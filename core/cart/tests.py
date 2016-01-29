from django.test import TestCase, RequestFactory
from django.http import HttpResponse

from lindshop.core.product.models import Product, ProductImage
from lindshop.core.category.models import Category
from lindshop.core.stock.models import Warehouse, Stock
from lindshop.core.pricing.models import Currency, Taxrule, Pricing
from lindshop.core.order.models import Order
from lindshop.core.customer.models import CustomerProfile, Country, Address
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.cart.views import addProduct, updateAmount, removeProduct, updateCart

# Create your tests here.
class CartTests(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.currency = Currency.objects.create(iso_code="SEK", format="%s kr", default=True)
		cls.taxrule = Taxrule.objects.create(name="25 Standard", percentage=25)
		cls.category = Category.objects.create(name="Men Shirts", slug="men-shirts")
		cls.product1 = Product.objects.create(name="Green T-shirt", slug="green-tshirt", category=cls.category, active=True)
		cls.product2 = Product.objects.create(name="Red T-shirt", slug="red-tshirt", category=cls.category, active=True)
		cls.pricing1 = Pricing.objects.create(product=cls.product1, currency=cls.currency, taxrule=cls.taxrule, price=79.2)
		cls.pricing2 = Pricing.objects.create(product=cls.product2, currency=cls.currency, taxrule=cls.taxrule, price=79.2)

		cls.factory = RequestFactory()

	def test_AddProductToCart(self):
		cart = Cart(currency=self.currency)
		cart.save()

		self.factory.session = {'id_cart': cart.pk} # Just make sure the factory got a session object.
		# Add a product to the cart, with correct data.
		# Should return True.
		addProduct(self.factory, self.product1.id)
		self.assertEqual(len(cart.cartitem_set.all()), 1) # It should now exist 1 item in the cart.

		try:
			addProduct(self.factory, 53) # Add product with wrong ID.
		except:
			pass

		# After adding a product with wrong id (above), it should still only be 1
		# item in the cart.
		self.assertEqual(len(cart.cartitem_set.all()), 1)

	def test_updateAmount(self):
		cart = Cart(currency=self.currency)
		cart.save()

		self.factory.session = {'id_cart': cart.pk} # Just make sure the factory got a session object.
		
		addProduct(self.factory, self.product1.id) # Add a product to the cart.

		self.assertEqual(cart.cartitem_set.get(product=self.product1).amount, 1) # Default amount after added should be 1.

		updateAmount(self.factory, cart.cartitem_set.get(product=self.product1).pk, 5) # Update amount to 5.

		self.assertEqual(cart.cartitem_set.get(product=self.product1).amount, 5) # Amount should be 5 after change.

	def test_removeProduct(self):
		from django.core.exceptions import ObjectDoesNotExist
		cart = Cart(currency=self.currency)
		cart.save()

		self.factory.session = {'id_cart': cart.pk} # Just make sure the factory got a session object.
		
		addProduct(self.factory, self.product1.id) # Add a product to the cart.

		self.assertEqual(cart.cartitem_set.get(product=self.product1).amount, 1) # Default amount after added should be 1.

		removeProduct(self.factory, cart.cartitem_set.get(product=self.product1).pk) # Remove the product that as just added.
		
		self.assertEqual(len(cart.cartitem_set.filter(product=self.product1)), 0) # After removing he product, it should not be found.