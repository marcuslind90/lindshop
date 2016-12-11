from django.core.management.base import BaseCommand, CommandError
from lindshop.core.demo.csv_importer import CSVImporter

class Command(BaseCommand):
	args = 'model'
	help = 'Importing default models data to the database from csv files located in /csv'

	def handle(self, *args, **options):

		if not args:
			self.import_categories()
			self.import_countries()
			self.import_currencies()
			self.import_taxrules()
			self.import_products()
			self.import_product_images()
			self.import_plans()
			self.import_pricings()
			self.import_carriers()
			self.import_carrier_pricing()
			self.import_attributes()
			self.import_attribute_choices()
			self.import_addresses()
			self.import_carts()
			self.import_cart_items()
			self.import_orders()

		elif 'category' in args:
			self.import_categories()

		elif 'country' in args:
			self.import_countries()

		elif 'currency' in args:
			self.import_currencies()

		elif 'taxrule' in args:
			self.import_taxrules()

		elif 'product' in args:
			self.import_products()

		elif 'productimage' in args:
			self.import_product_images()

		elif 'plan' in args:
			self.import_plans()

		elif 'pricing' in args:
			self.import_pricings()

		elif 'carrier' in args:
			self.import_carriers()

		elif 'carrierpricing' in args:
			self.import_carrier_pricing()

		elif 'attribute' in args:
			self.import_attributes()

		elif 'attributechoices' in args:
			self.import_attribute_choices()

		elif 'address' in args:
			self.import_addresses()

		elif 'cart' in args:
			self.import_carts()

		elif 'cart_item' in args:
			self.import_cart_items()

		elif 'order' in args:
			self.import_orders()

		else:
			raise CommandError("This model does not exist.")
		

	def import_categories(self):
		from lindshop.core.category.models import Category
		counter = Category.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/categories.csv")
			csvi.csv_to_model(model=Category)

			return True
		else:
			return False

	def import_countries(self):
		from lindshop.core.customer.models import Country
		counter = Country.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/countries.csv")
			csvi.csv_to_model(model=Country)

			return True
		else:
			return False

	def import_currencies(self):
		from lindshop.core.pricing.models import Currency
		counter = Currency.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/currencies.csv")
			csvi.csv_to_model(model=Currency)

			return True
		else:
			return False

	def import_taxrules(self):
		from lindshop.core.pricing.models import Taxrule
		counter = Taxrule.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/taxrules.csv")
			csvi.csv_to_model(model=Taxrule)

			return True
		else:
			return False

	def import_products(self):
		from lindshop.core.product.models import Product
		counter = Product.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/products.csv")
			csvi.csv_to_model(model=Product)

			return True
		else:
			return False

	def import_product_images(self):
		from lindshop.core.product.models import ProductImage
		counter = ProductImage.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/product_images.csv")
			csvi.csv_to_model(model=ProductImage)

			return True
		else:
			return False

	def import_plans(self):
		from lindshop.core.subscription.models import Plan
		counter = Plan.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/plans.csv")
			csvi.csv_to_model(model=Plan)

			return True
		else:
			return False

	def import_pricings(self):
		from lindshop.core.pricing.models import Pricing
		counter = Pricing.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/pricings.csv")
			csvi.csv_to_model(model=Pricing)

			return True
		else:
			return False

	def import_carriers(self):
		from lindshop.core.shipping.models import Carrier
		counter = Carrier.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/carriers.csv")
			csvi.csv_to_model(model=Carrier)

			return True
		else:
			return False

	def import_carrier_pricing(self):
		from lindshop.core.shipping.models import CarrierPricing
		counter = CarrierPricing.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/carrier_pricings.csv")
			csvi.csv_to_model(model=CarrierPricing)

			return True
		else:
			return False

	def import_attributes(self):
		from lindshop.core.attribute.models import Attribute
		counter = Attribute.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/attributes.csv")
			csvi.csv_to_model(model=Attribute)

			return True
		else:
			return False

	def import_attribute_choices(self):
		from lindshop.core.attribute.models import AttributeChoice
		counter = AttributeChoice.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/attribute_choices.csv")
			csvi.csv_to_model(model=AttributeChoice)

			return True
		else:
			return False

	def import_addresses(self):
		from lindshop.core.customer.models import Address
		counter = Address.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/addresses.csv")
			csvi.csv_to_model(model=Address)

			return True
		else:
			return False

	def import_carts(self):
		from lindshop.core.cart.models import Cart
		counter = Cart.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/carts.csv")
			csvi.csv_to_model(model=Cart)

			return True
		else:
			return False


	def import_cart_items(self):
		from lindshop.core.cart.models import CartItem
		counter = CartItem.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/cart_items.csv")
			csvi.csv_to_model(model=CartItem)

			return True
		else:
			return False

	def import_orders(self):
		from lindshop.core.order.models import Order
		counter = Order.objects.all()
		if len(counter) == 0:
			csvi = CSVImporter(filename="lindshop/core/demo/csv/orders.csv")
			csvi.csv_to_model(model=Order)

			return True
		else:
			return False