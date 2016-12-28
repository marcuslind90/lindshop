from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers

from lindshop.core.order.models import Order, CustomFieldValue, Notification
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.product.models import Product, ProductImage, ProductData, ProductDataPreset
from lindshop.core.customer.models import Address, Country
from lindshop.core.category.models import Category
from lindshop.core.pricing.models import Pricing, Taxrule, Currency, Voucher, Discount
from lindshop.core.attribute.models import Attribute, AttributeChoice
from lindshop.core.stock.models import Warehouse, Stock
from lindshop.core.menu.models import Menu, MenuItem
from lindshop.core.slideshow.models import Slideshow, Slide
from lindshop.core.shipping.models import Carrier, CarrierPricing

class DiscountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Discount
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}
		}

class VoucherSerializer(serializers.ModelSerializer):
	class Meta:
		model = Voucher
		fields = '__all__'

class CarrierPricingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CarrierPricing
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'carrier': {'required': False} # For CREATE calls the carrier ID is not set yet
		}

class CarrierSerializer(serializers.ModelSerializer):
	carrierpricing_set = CarrierPricingSerializer(many=True)
	class Meta:
		model = Carrier
		fields = ('id', 'name', 'delivery_text', 'logo', 'default', 'countries', 'carrierpricing_set')
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'logo': {'required': False}
		}

	def create(self, validated_data):
		# Seperate nested data from the Carrier object.
		pricings = validated_data.pop('carrierpricing_set')
		countries = validated_data.pop('countries')

		# Create our Carrier with the remaining data.
		carrier = Carrier.objects.create(**validated_data)

		# Use the nested `countries` data to add all the countries
		# to the ManyToMany `countryes`-field of Carrier.
		for country in countries:
			country_obj = Country.objects.get(pk=country.pk)
			carrier.countries.add(country_obj)

		# Use the nested `pricings` data and create all the new
		# pricings for the carrier.
		for pricing in pricings:
			CarrierPricing.objects.create(carrier=carrier, **pricing)

		return carrier

	def update(self, instance, validated_data):
		# Seperate nested data from the Carrier object.
		pricings = validated_data.pop('carrierpricing_set')
		countries = validated_data.pop('countries')

		# Initiate arrays that will store each ID that is included in the call
		# so that we can later remove all data stored in the DB that was not included.
		country_ids = []
		price_ids = []

		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		# Use the nested `pricings` data 
		for pricing in pricings:
			price_obj = CarrierPricing.objects.create(carrier=instance, **pricing)
			price_ids.append(price_obj.pk) # Keep the ID so that we remember which one was updated.

		# Use the nested `countries` data
		for country in countries:
			country_obj = Country.objects.get(pk=country.pk)
			instance.countries.add(country_obj)
			country_ids.append(country_obj.pk) # Keep the ID so that we remember which one was updated.

		# Get all the countries previously added to this instance and check
		# if any of them was NOT included in this call. If so, remove them. 
		for country in instance.countries.all():
			if country.id not in country_ids:
				instance.countries.remove(country)

		# Get all the pricings previously added to this instance and check
		# if any of them was NOT included in this call. If so, remove them. 
		for pricing in instance.carrierpricing_set.all():
			if pricing.id not in price_ids:
				instance.carrierpricing_set.remove(pricing)

		return instance

class SlideSerializer(serializers.ModelSerializer):
	class Meta:
		model = Slide
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'slideshow': {'required': False}, # Not required because the slideshow might not be saved yet
			'image': {'required': False}
		}

	def get_validation_exclusions(self):
			exclusions = super(SlideSerializer, self).get_validation_exclusions()
			return exclusions + ['id']

class SlideshowSerializer(serializers.ModelSerializer):
	slide_set = SlideSerializer(many=True)

	class Meta:
		model = Slideshow
		fields = ('id', 'name', 'slide_set')

	def create(self, validated_data):
		slides = validated_data.pop('slide_set')
		slideshow = Slideshow.objects.create(**validated_data)

		# Use the nested `slides` data to create each slide
		for item in slides:
			Slide.objects.create(slideshow=slideshow, **item)

		return slideshow

	def update(self, instance, validated_data):
		# Seperate nested data
		slides = validated_data.pop('slide_set')

		# Initiate array that will store each ID that is included in the call
		# so that we can later remove all data stored in the DB that was not included.
		item_ids = []

		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		# Update the nested `slides` data
		for item in slides:
			# If the slide already has an `id` it means the Slide already
			# exists and should be UPDATED.
			if 'id' in item:
				item_obj = Slide.objects.get(pk=item['id'])
				for(key, value) in item.items():
					setattr(item_obj, key, value)

				item_obj.save()

			# If no `id` exist it means the slide is new and should be CREATED.
			else:
				item_obj = Slide.objects.create(slideshow=instance, **item)

			# Save the ID of the slide so we know which ones were included in the call.
			item_ids.append(item_obj.id)

		# If this instance have any other slides that was not send
		# in this request, then remove them. They should be deleted.
		for item in instance.slide_set.all():
			if item.id not in item_ids:
				item.delete()

		return instance

class MenuItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = MenuItem
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'menu': {'required': False} # Not required because the `menu` might not be saved yet.
		}

	def get_validation_exclusions(self):
			exclusions = super(MenuItemSerializer, self).get_validation_exclusions()
			return exclusions + ['id']

class MenuSerializer(serializers.ModelSerializer):
	menuitem_set = MenuItemSerializer(many=True)
	class Meta:
		model = Menu
		fields = ('id', 'name', 'menuitem_set')

	def create(self, validated_data):
		menu_items = validated_data.pop('menuitem_set')

		menu = Menu.objects.create(**validated_data)

		# Create the items of the menu with the nested data.
		for item in menu_items:
			MenuItem.objects.create(menu=menu, **item)

		return menu

	def update(self, instance, validated_data):
		# Seperate nested data
		menu_items = validated_data.pop('menuitem_set')

		# Initiate array that will be used to store the ID's of all items
		# that are updated, so that we can remove any items not included
		# in the current call, but existing in the database.
		item_ids = []

		# Update the instance with the data from the request.
		for(key, value) in validated_data.items():
			setattr(instance, key, value)

		instance.save()

		# Use the nested data and create the items of the menu.
		for item in menu_items:
			# If the item has an ID, it means it already exists and should be UPDATED.
			if 'id' in item:
				item_obj = MenuItem.objects.get(pk=item['id'])
				for(key, value) in item.items():
					setattr(item_obj, key, value)

				item_obj.save()
			# If the item has no ID, it means it should be CREATED.
			else:
				item_obj = MenuItem.objects.create(menu=instance, **item)

			# Store the value of each updated/created item 
			item_ids.append(item_obj.id)

		# Check all items in the database of this menu, and remove any item
		# that was not included in this call.
		for item in instance.menuitem_set.all():
			if item.id not in item_ids:
				item.delete()

		return instance

class WarehouseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Warehouse
		fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'

class AttributeChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = AttributeChoice
		fields = '__all__'
		# We need to have it read_only=false to keep it in validated_data
		# but we keep it required=false so that we can leave out the id when
		# We want to create a NEW attributechoice with unknown ID (Because not created yet).
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'attribute': {'required': False} # We also set attribute to false for same reason.
		}

	def get_validation_exclusions(self):
			exclusions = super(AttributeChoiceSerializer, self).get_validation_exclusions()
			return exclusions + ['id']

class AttributeSerializer(serializers.ModelSerializer):
	attributechoice_set = AttributeChoiceSerializer(many=True)
	class Meta:
		model = Attribute
		fields = ('id', 'name', 'text_input', 'slug', 'product', 'attributechoice_set')
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
		}

	def update(self, instance, validated_data):
		choice_data = validated_data.pop('attributechoice_set')
		# We keep a list of our Choice id's so we can delete any choice that
		# is not included in the request. 
		choice_ids = []  

		for choice in choice_data:
			# If id is within the call, then update the object with matching id
			if 'id' in choice:
				try:
					choice_obj = AttributeChoice.objects.get(pk=choice['id'])
					choice_obj.value = choice['value']
					choice_obj.slug = choice['slug']
					choice_obj.attribute = instance
				# If ID is not found, then create a new object
				except AttributeChoice.DoesNotExist:
					choice.pop('id')
					choice_obj = AttributeChoice(**choice)
			# If no ID within the call, create a new object.
			else:
				choice_obj = AttributeChoice(**choice)

			choice_obj.save()

			choice_ids.append(choice_obj.id)
		
		# Now delete all other entries that was NOT updated.
		# Meaning... If there was any attributechoices NOT included in our call (= They've been deleted)
		# Then delete them from the database.
		for choice in instance.attributechoice_set.all():
			if choice.id not in choice_ids:
				choice.delete()

		return instance

	def create(self, validated_data):
		# Seperate nested data...
		choice_data = validated_data.pop('attributechoice_set')

		# Create the Attribute with remaining data.
		attribute = Attribute(**validated_data)
		attribute.save()

		# Create the AttributeChoices with the nested data seperated above.
		for choice in choice_data:
			choice_obj = AttributeChoice(attribute=attribute, **choice)
			choice_obj.save()

		return attribute

class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'product': {'required': False}, 
			'image': {'required': False}
		}

class CurrencySerializer(serializers.ModelSerializer):
	class Meta:
		model = Currency
		fields = '__all__'

class TaxruleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Taxrule
		fields = '__all__'

class PricingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pricing
		fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Country
		fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
	country = CountrySerializer()
	class Meta:
		model = Address
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'email', 'first_name', 'last_name', 'user_address')

class ProductDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductData
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'product': {'required': False}
		}

class ProductDataPresetSerializer(serializers.ModelSerializer):
	data = ProductDataSerializer(many=True)
	class Meta:
		model = ProductDataPreset
		fields = '__all__'

	def create(self, validated_data):
		# Seperate nessted data
		data = validated_data.pop('data')

		preset = ProductDataPreset.objects.create(**validated_data)

		# The data in the request come from an already existing product.
		# We first need to unset the `id` and `product` value from the data
		# to make sure we created new and blank entries to the Preset that
		# can be used in the future with any other product.
		for d in data:
			if 'id' in d:
				d.pop('id')
				d.pop('product')

			data_obj = ProductData.objects.create(**d)
			preset.data.add(data_obj) # Add to ManyToManyField.

		return preset

class ProductSerializer(serializers.ModelSerializer):
	attribute_set = AttributeSerializer(many=True)
	productimage_set = ProductImageSerializer(many=True)
	productdata_set = ProductDataSerializer(many=True)
	discount_set = DiscountSerializer(many=True)
	price = serializers.ReadOnlyField(source='get_price_incl')

	class Meta:
		model = Product
		fields = (
			'id', 
			'name', 
			'productimage_set', 
			'short_description', 
			'description', 
			'slug', 
			'active', 
			'seo_title', 
			'seo_description', 
			'category', 
			'categories', 
			'stock', 
			'attribute_set', 
			'pricing_set', 
			'productdata_set', 
			'discount_set', 
			'price'
		)

	def create(self, validated_data):
		# Seperate nested data
		if 'attribute_set' in validated_data:
			validated_data.pop('attribute_set')
		if 'pricing_set' in validated_data:
			validated_data.pop('pricing_set')
		if 'stock' in validated_data:
			validated_data.pop('stock')
		if 'productimage_set' in validated_data:
			validated_data.pop('productimage_set')
		if 'productdata_set' in validated_data:
			validated_data.pop('productdata_set')

		categories_data = validated_data.pop('categories')

		product = Product.objects.create(**validated_data)

		for category in categories_data:
			product.categories.add(category)

		return product

	def update(self, instance, validated_data):
		# Seperate nested data
		if 'attribute_set' in validated_data:
			attribute_data = validated_data.pop('attribute_set')
			self.add_attribute_data(instance, attribute_data)
		if 'pricing_set' in validated_data:
			pricing_data = validated_data.pop('pricing_set')
		if 'stock' in validated_data:
			stock_data = validated_data.pop('stock')
		if 'productimage_set' in validated_data:
			image_data = validated_data.pop('productimage_set')
			self.add_image_data(instance, image_data)
		if 'productdata_set' in validated_data:
			productdata_data = validated_data.pop('productdata_set')
			self.add_productdata_data(instance, productdata_data)
		if 'discount_set' in validated_data:
			discount_data = validated_data.pop('discount_set')
			self.add_discount_data(discount_data)

		
		#add_pricing_data(instance, pricing_data)
		#add_stock_data(instance, stock_data)

		# Iterate through all data in validated_data and update the instance
		# with new values and save it.
		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		return instance

	def add_discount_data(self, validated_data):
		data_ids = []
		for discount in validated_data:
			if 'id' in discount:
				instance = Discount.objects.get(pk=discount['id'])
				DiscountSerializer().update(instance, discount)
			else:
				instance = DiscountSerializer().create(discount)

			data_ids.append(instance.id)

		# TODO: This can be refactored. This type of code is used a lot.
		for data in Discount.objects.filter(product=instance.product):
			if data.id not in data_ids:
				data.delete()

		return instance

	def add_productdata_data(self, instance, validated_data):
		# Initiate array that keep all id's that is included in the call 
		# so that we later know which ones NOT included and that should be
		# deleted from the database.
		data_ids = []

		for data in validated_data:
			# If an ID already exists it means that the entry should be UPDATED.
			if 'id' in data:
				data_obj = ProductData.objects.get(pk=data['id'])

				for(key, value) in data.items():
					setattr(data_obj, key, value)
				data_obj.save()

			# If no ID exists, it means that the entry should be CREATED.
			else:
				data_obj = ProductData.objects.create(product=instance, **data)

			data_ids.append(data_obj.id)

		# Check existing entries in the database with the actual entries that were
		# included in the request. If they were NOT included in the request, it means 
		# that the user removed them, and they should be deleted from the database.
		for data in instance.productdata_set.all():
			if data.id not in data_ids:
				data.delete()

		return instance

	def add_image_data(self, instance, validated_data):
		image_ids = []

		for image in validated_data:
			# If an ID already exists it means that the entry should be UPDATED.
			if 'id' in image:
				image_obj = ProductImage.objects.get(pk=image['id'])
				for(key, value) in image.items():
					setattr(image_obj, key, value)

				image_obj.save()

			# If no ID exists, it means that the entry should be CREATED.
			else:
				image_obj = ProductImage.objects.create(product=instance, **image)

			image_ids.append(image_obj.id)

		# Check existing entries in the database with the actual entries that were
		# included in the request. If they were NOT included in the request, it means 
		# that the user removed them, and they should be deleted from the database.
		for image in instance.productimage_set.all():
			if image.id not in image_ids:
				image.delete()

		return instance

	def add_attribute_data(self, instance, validated_data):
		attribute_ids = []

		# Handle nested attribute values.
		for attribute in validated_data:
			# If an ID already exists it means that the entry should be UPDATED.
			if 'id' in attribute:
				attribute_instance = Attribute.objects.get(pk=attribute['id'])
				self.update_attribute(attribute_instance, attribute)

			# If no ID exists, it means that the entry should be CREATED.
			else:
				attribute_instance = self.create_attribute(instance, attribute)

			attribute_ids.append(attribute_instance.pk)

		# Check existing entries in the database with the actual entries that were
		# included in the request. If they were NOT included in the request, it means 
		# that the user removed them, and they should be deleted from the database.
		for attribute in instance.attribute_set.all():
			if attribute.id not in attribute_ids:
				attribute.delete()

		return instance

	def update_attribute(self, instance, validated_data):
		choice_data = validated_data.pop('attributechoice_set')
		choice_ids = []  

		validated_data['slug'] = slugify(validated_data['name'])

		# Update the existing values of the instance with the values from
		# the request, and save it to the database.
		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		for choice in choice_data:
			# If an ID already exists it means that the entry should be UPDATED.
			if 'id' in choice:
				try:
					choice_obj = AttributeChoice.objects.get(pk=choice['id'])
					choice_obj.value = choice['value']
					choice_obj.slug = slugify(choice['value'])
					choice_obj.attribute = instance
				# If no ID exists, it means that the entry should be CREATED.
				except AttributeChoice.DoesNotExist:
					choice.pop('id')
					choice_obj = AttributeChoice(**choice)
			# If no ID exists, it means that the entry should be CREATED.
			else:
				choice_obj = AttributeChoice(**choice)

			choice_obj.save()

			choice_ids.append(choice_obj.id)
		
		# Check existing entries in the database with the actual entries that were
		# included in the request. If they were NOT included in the request, it means 
		# that the user removed them, and they should be deleted from the database.
		for choice in instance.attributechoice_set.all():
			if choice.id not in choice_ids:
				choice.delete()

		return instance

	def create_attribute(self, instance, validated_data):
		choice_data = validated_data.pop('attributechoice_set')
		validated_data['slug'] = slugify(validated_data['name'])

		attribute = Attribute(**validated_data)
		attribute.save()

		for choice in choice_data:
			choice_obj = AttributeChoice(attribute=attribute, **choice)
			choice_obj.save()

		return attribute

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
	product = ProductSerializer(read_only=True)
	price = serializers.ReadOnlyField(source='get_total')
	class Meta:
		model = CartItem
		depth = 1
		fields = (
			'amount', 
			'product', 
			'attribute', 
			'price',  
		)

class CartSerializer(serializers.ModelSerializer):
	cartitem_set = CartItemSerializer(read_only=True, many=True)
	total = serializers.ReadOnlyField(source='get_total')
	class Meta:
		model = Cart
		fields = (
			'id', 
			'date_created', 
			'voucher', 
			'carrier', 
			'currency', 
			'cartitem_set', 
			'total', 
		)

class CustomFieldValueSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomFieldValue
		depth = 1
		exclude = ('id', 'order')

class OrderSerializer(serializers.ModelSerializer):
	cart = CartSerializer()
	class Meta:
		model = Order
		fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
	total = serializers.ReadOnlyField(source='get_total')
	class Meta:
		model = Order
		fields = '__all__'