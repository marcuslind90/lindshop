from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from lindshop.core.cart.models import Cart
from lindshop.core.customer.models import Country
from lindshop.core.product.models import Product
from lindshop.core.category.models import Category
from lindshop.core.pricing.models import Currency, Taxrule, Pricing
from lindshop.core.stock.models import Warehouse
from lindshop.core.checkout.views import checkout
from lindshop.core.dashboard import api
# Create your tests here.
class ViewTests(TestCase):

	@classmethod
	def setUpTestData(self):
		self.country = Country.objects.create(name="Thailand", slug="thailand", default=True)
		self.currency = Currency.objects.create(iso_code="SEK", format="%s kr", default=True)
		self.cart 	= Cart.objects.create(currency=self.currency)
		self.taxrule = Taxrule.objects.create(name="25 Standard", percentage=25)
		self.category = Category.objects.create(name="Men Shirts", slug="men-shirts")
		self.product1 = Product.objects.create(name="Green T-shirt", slug="green-tshirt", category=self.category, active=True)
		self.product2 = Product.objects.create(name="Red T-shirt", slug="red-tshirt", category=self.category, active=True)
		self.pricing1 = Pricing.objects.create(product=self.product1, currency=self.currency, taxrule=self.taxrule, price=79.2)
		self.pricing2 = Pricing.objects.create(product=self.product2, currency=self.currency, taxrule=self.taxrule, price=79.2)
		self.normaluser = get_user_model().objects.create_user(username="normaluser", email="normaluser@mail.com", password="normaluser")
		self.adminuser = get_user_model().objects.create_user(username="adminuser", email="adminuser@mail.com", password="adminuser", is_staff=True)
		self.warehouse = Warehouse.objects.create(name="Test Warehouse", address="Main Street 13", country=self.country, default=True)

		self.factory = RequestFactory(enforce_csrf_checks=False)
		self.factory.session = {'id_cart': self.cart.pk}
		self.factory.META = {'CSRF_COOKIE_USED': False, 'CSRF_COOKIE_SECURE': False}

	def test_api_auth(self):
		response = self.client.get(reverse('lindshop:api:Product-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_users_auth(self):
		response = self.client.get(reverse('lindshop:api:User-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:User-list'))
		request.user = self.normaluser

		view = api.UserViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_users_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:User-list'), {
			"email": "test@test.com",
			"first_name": "Test",
			"last_name": "Test",
			"user_address": []
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.


	def test_api_orders(self):
		response = self.client.get(reverse('lindshop:api:Order-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_orders_auth(self):
		response = self.client.get(reverse('lindshop:api:Order-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Order-list'))
		request.user = self.normaluser

		view = api.OrderViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	"""def test_api_orders_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Order-list'), {
			"email": "test@test.com",
			"first_name": "Test",
			"last_name": "Test",
			"user_address": []
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'."""

	def test_api_carts(self):
		response = self.client.get(reverse('lindshop:api:Cart-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_carts_auth(self):
		response = self.client.get(reverse('lindshop:api:Cart-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Cart-list'))
		request.user = self.normaluser

		view = api.CartViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	"""def test_api_carts_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Cart-list'), {
			"email": "test@test.com",
			"first_name": "Test",
			"last_name": "Test",
			"user_address": []
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'."""

	def test_api_products(self):
		response = self.client.get(reverse('lindshop:api:Product-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_products_auth(self):
		response = self.client.get(reverse('lindshop:api:Product-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Product-list'))
		request.user = self.normaluser

		view = api.ProductViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_products_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Product-list'), {
			"name": "Test",
			"productimage_set": [],
			"short_description": "",
			"description": "",
			"slug": "test",
			"active": False,
			"seo_title": "",
			"seo_description": "",
			"category": "",
			"categories": [],
			"stock": 10, 
			"attribute_set": [],
			"pricing_set": [],
			"productdata_set": [], 
			"discount_set": []
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_categories(self):
		response = self.client.get(reverse('lindshop:api:Category-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_categories_auth(self):
		response = self.client.get(reverse('lindshop:api:Category-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Category-list'))
		request.user = self.normaluser

		view = api.CategoryViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_categories_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Category-list'), {
			"name": "Test",
			"description": "",
			"image": "",
			"slug": "test",
			"parent": ""
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_pricings(self):
		response = self.client.get(reverse('lindshop:api:Pricing-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_pricings_auth(self):
		response = self.client.get(reverse('lindshop:api:Pricing-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Pricing-list'))
		request.user = self.normaluser

		view = api.PricingViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_pricings_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Pricing-list'), {
			"price": 1,
			"product": 1,
			"plan": "",
			"currency": 1,
			"taxrule": 1
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_taxrules(self):
		response = self.client.get(reverse('lindshop:api:Taxrule-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_taxrules_auth(self):
		response = self.client.get(reverse('lindshop:api:Taxrule-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Taxrule-list'))
		request.user = self.normaluser

		view = api.TaxruleViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_taxrules_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Taxrule-list'), {
			"name": "Test",
			"percentage": 1
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_currencies(self):
		response = self.client.get(reverse('lindshop:api:Currency-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_currencies_auth(self):
		response = self.client.get(reverse('lindshop:api:Currency-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Currency-list'))
		request.user = self.normaluser

		view = api.CurrencyViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_currencies_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Currency-list'), {
			"iso_code": "THB",
			"format": "%s THB",
			"default": False,
			"language": "th"
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_images(self):
		response = self.client.get(reverse('lindshop:api:ProductImage-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_images_auth(self):
		response = self.client.get(reverse('lindshop:api:ProductImage-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:ProductImage-list'))
		request.user = self.normaluser

		view = api.ProductImageViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	"""def test_api_images_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:ProductImage-list'), {
			"email": "test@test.com",
			"first_name": "Test",
			"last_name": "Test",
			"user_address": []
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'."""

	def test_api_attributes(self):
		response = self.client.get(reverse('lindshop:api:Attribute-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_attributes_auth(self):
		response = self.client.get(reverse('lindshop:api:Attribute-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Attribute-list'))
		request.user = self.normaluser

		view = api.AttributeViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_attributes_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Attribute-list'), {
			"name": "Size",
			"text_input": True,
			"slug": "size",
			"product": 1,
			"attributechoice_set": [
				{
					"value": "Blue",
					"slug": "blue"
				}
            ]
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_warehouses(self):
		response = self.client.get(reverse('lindshop:api:Warehouse-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_warehouses_auth(self):
		response = self.client.get(reverse('lindshop:api:Warehouse-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Warehouse-list'))
		request.user = self.normaluser

		view = api.WarehouseViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_warehouses_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Warehouse-list'), {
			"name": "Test", 
			"address": "Hello", 
			"country": 1, 
			"default": True
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_stock(self):
		response = self.client.get(reverse('lindshop:api:Stock-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_stock_auth(self):
		response = self.client.get(reverse('lindshop:api:Stock-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Stock-list'))
		request.user = self.normaluser

		view = api.StockViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_stock_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Stock-list'), {
			"stock": 1,
			"shelf": "E4",
			"product": 1,
			"warehouse": 1
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_menus(self):
		response = self.client.get(reverse('lindshop:api:Menu-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_menus_auth(self):
		response = self.client.get(reverse('lindshop:api:Menu-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Menu-list'))
		request.user = self.normaluser

		view = api.MenuViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_menus_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Menu-list'), {
			"name": "Menu",
			"menuitem_set": [
				{
					"item_type": "category", 
					"object_id": 1, 
					"label": "", 
					"url": ""	
				}
			]
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_slideshows(self):
		response = self.client.get(reverse('lindshop:api:Slideshow-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_slideshows_auth(self):
		response = self.client.get(reverse('lindshop:api:Slideshow-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Slideshow-list'))
		request.user = self.normaluser

		view = api.SlideshowViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	"""def test_api_slideshow_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Slideshow-list'), {
			"name": "TestSlideshow",
			"slide_set": []
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'."""

	def test_api_productdatapresets(self):
		response = self.client.get(reverse('lindshop:api:DataPreset-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_productdatapresets_auth(self):
		response = self.client.get(reverse('lindshop:api:DataPreset-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:DataPreset-list'))
		request.user = self.normaluser

		view = api.ProductDataPresetViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_productdatapresets_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:DataPreset-list'), {
			"data": [
				{
					"label": "Data", 
					"value": "Value"
				}
			],
			"label": "MyPreset"
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_countries(self):
		response = self.client.get(reverse('lindshop:api:Country-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_countries_auth(self):
		response = self.client.get(reverse('lindshop:api:Country-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Country-list'))
		request.user = self.normaluser

		view = api.CountryViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_countries_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Country-list'), {
			"name": "Sweden",
			"slug": "sweden",
			"default": False
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.

	def test_api_carriers(self):
		response = self.client.get(reverse('lindshop:api:Carrier-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

	def test_api_carriers_auth(self):
		response = self.client.get(reverse('lindshop:api:Carrier-list'))
		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because not yet Authenticated.

		request = self.factory.get(reverse('lindshop:api:Carrier-list'))
		request.user = self.normaluser

		view = api.CarrierViewSet.as_view(actions={'get': 'list'})
		response = view(request)

		self.assertEqual(response.status_code, 403) # Should return 403 Permission Denied because User is not Admin.

		request.user = self.adminuser
		response = view(request)
		self.assertEqual(response.status_code, 200) # Should return 200 because we're now Admin.

	def test_api_carriers_create(self):
		client = Client()
		client.login(username="adminuser", password="adminuser")

		response = client.post(reverse('lindshop:api:Carrier-list'), {
			"name": "Schenker",
			"delivery_text": "3-5 days",
			"logo": "",
			"default": False,
			"countries": [1],
			"carrierpricing_set": []
		})

		self.assertEqual(response.status_code, 201) # Should return 201 which means 'Created'.