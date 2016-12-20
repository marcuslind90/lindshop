from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from django.contrib.auth.models import User
from django.http import JsonResponse

from lindshop.core.order.models import Order, CustomFieldValue, Notification
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.product.models import Product, ProductImage, ProductData, ProductDataPreset
from lindshop.core.customer.models import Address, Country
from lindshop.core.category.models import Category
from lindshop.core.pricing.models import Pricing, Taxrule, Currency
from lindshop.core.attribute.models import Attribute, AttributeChoice
from lindshop.core.stock.models import Warehouse, Stock
from lindshop.core.menu.models import Menu, MenuItem
from lindshop.core.slideshow.models import Slideshow, Slide
from lindshop.core.shipping.models import Carrier, CarrierPricing

import json
import re
from StringIO import StringIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# REST API Url Patterns (Used by AngularJS)
# Serializers define the API representation.
class CarrierPricingSerializer(serializers.ModelSerializer):
	"""CarrierPricing used in the CarrierSerializer. 
	Handles how CarrierPricing is displayed from the API.
	"""
	class Meta:
		model = CarrierPricing
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'carrier': {'required': False} # For CREATE calls the carrier ID is not set yet
		}

class CarrierSerializer(serializers.ModelSerializer):
	"""Handles how the Carrier data is displayed from the API.
	Also handles custom CREATE and UPDATE calls.
	"""
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

		# Loop through our items in the call, and set matching Instance parameter to its value
		for(key, value) in validated_data.items():
			setattr(instance, key, value)

		# Save the instance. This updates the database.
		instance.save()

		# Use the nested `pricings` data and create all the new
		# pricings for the carrier.
		for pricing in pricings:
			price_obj = CarrierPricing.objects.create(carrier=instance, **pricing)
			price_ids.append(price_obj.pk) # Keep the ID so that we remember which one was updated.

		# Use the nested `countries` data to add all the countries
		# to the ManyToMany `countryes`-field of Carrier.
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


class CarrierViewSet(viewsets.ModelViewSet):
	"""The ViewSet of the Carrier object. This handles the request and
	sends it to the serializer.
	"""
	serializer_class = CarrierSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Carrier.objects.all()

		return queryset

	def create(self, request, pk=None):

		# If `logo` is included in the call, it means an Image is uploaded.
		# The image from AngularJS is stored as a  base64 string. We use the string and 
		# create an image of it and then replace the original base64 string stored in the request
		# with the new image.
		if 'logo' in request.data and request.data['logo'] is not None and request.data['logo'] != "":
			img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", request.data['logo']).groupdict()
			blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
			image = StringIO(blob)
			image = InMemoryUploadedFile(image, None, request.data['filename'], 'image/jpeg', image.len, None)

			request.data['logo'] = image # Replace the original base64 string with the new file.

		carrier = Carrier(pk=pk)

		# Sends the data to the serializer that validates the data and stores it.
		serialized = self.serializer_class(carrier, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'ERROR': serialized.errors})

	def update(self, request, pk=None):

		# If `logo` is included in the call, it means an Image is uploaded.
		# The image from AngularJS is stored as a  base64 string. We use the string and 
		# create an image of it and then replace the original base64 string stored in the request
		# with the new image.
		if 'logo' in request.data and request.data['logo'] is not None and request.data['logo'] != "":

			# To see if it's an already existing image, or a new one, we check if the logo-value
			# is an URL (to an existing, uploaded image) or a base64 encoded string (a new uploaded file)
			validator = URLValidator()
			try:
				# Validate that it's an URL. If it is, it means that the image is already stored
				# and NOT a new uploaded image. So leave it alone.
				validator(request.data['logo'])
				request.data.pop('logo')
			
			# If we get an Exception for the value NOT being a URL, we should handle Image Upload...
			except ValidationError:
				img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", request.data['logo']).groupdict()
				blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
				image = StringIO(blob)
				image = InMemoryUploadedFile(image, None, request.data['filename'], 'image/jpeg', image.len, None)

				# Replace the base64-string value with the new file.
				request.data['logo'] = image

		# If 'logo' is included, but its "None". Then remove it (So it doesn't replace existing value with None).
		elif 'logo' in request.data and request.data['logo'] is None:
			request.data.pop('logo')

		# Get the Instance of the Carrier we're updating...
		carrier = Carrier.objects.get(pk=pk)
		serialized = self.serializer_class(carrier, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data)
		else:
			return Response(serialized.data)

class SlideSerializer(serializers.ModelSerializer):
	"""Serializer that handle Slide's of a Slideshow from the API
	"""
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
	"""Serializer that handle Slideshow's from the API
	"""
	slide_set = SlideSerializer(many=True)

	class Meta:
		model = Slideshow
		fields = ('id', 'name', 'slide_set')

	def create(self, validated_data):
		"""Handle CREATE calls of Slideshow to the API
		"""

		# Seperate nested data
		slides = validated_data.pop('slide_set')

		# Create a new Slideshow object with the remaining data.
		slideshow = Slideshow.objects.create(**validated_data)

		# Use the nested `slides` data to create each slide
		for item in slides:
			Slide.objects.create(slideshow=slideshow, **item)

		return slideshow

	def update(self, instance, validated_data):
		"""Handle UPDATE calls of Slideshow to the API
		"""

		# Seperate nested data
		slides = validated_data.pop('slide_set')

		# Initiate array that will store each ID that is included in the call
		# so that we can later remove all data stored in the DB that was not included.
		item_ids = []

		# Iterate through all data in validated_data and update the instance
		# with new values and save it.
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

class SlideshowViewSet(viewsets.ModelViewSet):
	serializer_class = SlideshowSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Slideshow.objects.all()

		return queryset

	def create(self, request, pk=None):
		# Seperate nested data
		slides = request.data.pop('slide_set')

		# For each slide that is being created, we create a new file by using the base64 data send in the request
		# and then replace the original value with the new file.
		for slide in slides:
			img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", slide['image']).groupdict()
			blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
			image = StringIO(blob)
			image = InMemoryUploadedFile(image, None, slide['filename'], 'image/jpeg', image.len, None)
			
			slide['image'] = image

		request.data['slide_set'] = slides

		slideshow = Slideshow(pk=pk)
		serialized = self.serializer_class(slideshow, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

	def update(self, request, pk=None):
		# Seperate nested data
		slides = request.data.pop('slide_set')

		# Since this is an UPDATE called it means that the slideshow might already have slides
		# created with images already uploaded. We check if the value is an existing or a new image by 
		# validating if it is an URL or not (Already uploaded images will point to an URL while new images
		# is an base64 encoded string).
		validator = URLValidator()
		for slide in slides:
			try:
				validator(slide['image'])
				# Since it's an already existing image, we don't have to update it, so remove it.
				slide.pop('image')

			# If validation fails, create the file from the data.
			except ValidationError:
				img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", slide['image']).groupdict()
				blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
				image = StringIO(blob)
				image = InMemoryUploadedFile(image, None, slide['filename'], 'image/jpeg', image.len, None)
				slide['image'] = image

		request.data['slide_set'] = slides

		slideshow = Slideshow(pk=pk)
		serialized = self.serializer_class(slideshow, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response({'status': 'UPDATED', 'image_data': serialized.data})
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

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
		# Seperate nested data
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


class MenuViewSet(viewsets.ModelViewSet):
	serializer_class = MenuSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Menu.objects.all()

		return queryset

class WarehouseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Warehouse
		fields = '__all__'

	def create(self, validated_data):
		warehouse = Warehouse(**validated_data)
		warehouse.save()

		# If the instance updated is set to default, then unset "default"
		# from any other warehouse (there can only be 1 default).
		if warehouse.default:
			warehouses = Warehouse.objects.all().exclude(pk=warehouse.pk)
			warehouses.update(default=False)

		return country

	def update(self, instance, validated_data):
		# Update the instance with the new data from the request.
		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		# If the instance updated is set to default, then unset "default"
		# from any other country (there can only be 1 default).
		if instance.default:
			warehouses = Warehouse.objects.all().exclude(pk=instance.pk)
			warehouses.update(default=False)

		return instance

class WarehouseViewSet(viewsets.ModelViewSet):
	serializer_class = WarehouseSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Warehouse.objects.all()

		return queryset

class StockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'

class StockViewSet(viewsets.ModelViewSet):
	serializer_class = StockSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Stock.objects.all()
		product = self.request.query_params.get('product', None)
		warehouse = self.request.query_params.get('warehouse', None)

		if product:
			queryset = queryset.filter(product=product)
		if warehouse:
			queryset = queryset.filter(warehouse=warehouse)

		return queryset

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

class AttributeViewSet(viewsets.ModelViewSet):
	serializer_class = AttributeSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Attribute.objects.all()
		product = self.request.query_params.get('product', None)
		if product:
			queryset = queryset.filter(product=product)

		return queryset

	def update(self, request, pk=None):
		attribute = Attribute(pk=pk)
		serialized = self.serializer_class(attribute, data=request.data, partial=True)
		
		# Slugify all Values into the slug-field.
		for choice in request.data['attributechoice_set']:
			choice['slug'] = slugify(choice['value'])

		if serialized.is_valid():
			serialized.save()
			return Response({'status': 'UPDATED'})
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = '__all__'
		extra_kwargs = {
			'id': {'read_only': False, 'required': False}, 
			'product': {'required': False}, 
			'image': {'required': False}
		}

class ProductImageViewSet(viewsets.ModelViewSet):
	serializer_class = ProductImageSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = ProductImage.objects.all()
		product = self.request.query_params.get('product', None)
		featured = self.request.query_params.get('featured', None)
		if product:
			queryset = queryset.filter(product=product)
		if featured:
			queryset = queryset.filter(featured=True)

		return queryset

	def create(self, request, pk=None):
		# The newly uploaded image is stored as a base64 string. We use the data to create a new file
		# and then replace the original base64 string with the newly created file.
		img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", request.data['image']).groupdict()
		blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
		image = StringIO(blob)
		image = InMemoryUploadedFile(image, None, request.data['filename'], 'image/jpeg', image.len, None)

		request.data['image'] = image

		image = ProductImage(pk=pk)
		serialized = self.serializer_class(image, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

class CurrencySerializer(serializers.ModelSerializer):
	"""Custom CurrencySerializer that handles saves and updates of
	new currencies. When a currency is set to default, it unset every other
	currency that is default.
	"""
	class Meta:
		model = Currency
		fields = '__all__'

	def create(self, validated_data):
		currency = Currency(**validated_data)
		currency.save()

		# If the instance updated is set to default, then unset "default"
		# from any other currency (there can only be 1 default).
		if currency.default:
			currencies = Currency.objects.all().exclude(pk=currency.pk)
			currencies.update(default=False)

		return currency

	def update(self, instance, validated_data):
		# Update the instance with the new data...
		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		# If the instance updated is set to default, then unset "default"
		# from any other currency (there can only be 1 default).
		if instance.default:
			currencies = Currency.objects.all().exclude(pk=instance.pk)
			currencies.update(default=False)

		return instance

class CurrencyViewSet(viewsets.ModelViewSet):
	serializer_class = CurrencySerializer
	queryset = Currency.objects.all()
	permission_classes = (IsAdminUser,)

class TaxruleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Taxrule
		fields = '__all__'

class TaxruleViewSet(viewsets.ModelViewSet):
	serializer_class = TaxruleSerializer
	queryset = Taxrule.objects.all()
	permission_classes = (IsAdminUser,)

class PricingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pricing
		fields = '__all__'

class PricingViewSet(viewsets.ModelViewSet):
	serializer_class = PricingSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Pricing.objects.all()
		product = self.request.query_params.get('product', None)
		if product:
			queryset = queryset.filter(product=product)

		return queryset

class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Country
		fields = '__all__'

	def create(self, validated_data):
		country = Country(**validated_data)
		country.save()

		# If the instance updated is set to default, then unset "default"
		# from any other country (there can only be 1 default).
		if country.default:
			countries = Country.objects.all().exclude(pk=country.pk)
			countries.update(default=False)

		return country

	def update(self, instance, validated_data):
		# Update the instance with the new data from the request.
		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		# If the instance updated is set to default, then unset "default"
		# from any other country (there can only be 1 default).
		if instance.default:
			countries = Country.objects.all().exclude(pk=instance.pk)
			countries.update(default=False)

		return instance

class CountryViewSet(viewsets.ModelViewSet):
	queryset = Country.objects.all()
	serializer_class = CountrySerializer
	permission_classes = (IsAdminUser,)

class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		depth = 1
		exclude = ('user', )

class UserSerializer(serializers.ModelSerializer):
	user_address = AddressSerializer(read_only=True, many=True)
	class Meta:
		model = User
		depth = 1
		fields = ('id', 'email', 'first_name', 'last_name', 'user_address')

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (IsAdminUser,)

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

class ProductDataPresetViewSet(viewsets.ModelViewSet):
	queryset = ProductDataPreset.objects.all()
	serializer_class = ProductDataPresetSerializer
	permission_classes = (IsAdminUser,)

class ProductSerializer(serializers.ModelSerializer):
	attribute_set = AttributeSerializer(many=True)
	productimage_set = ProductImageSerializer(many=True)
	productdata_set = ProductDataSerializer(many=True)

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
			'productdata_set'
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

		
		#add_pricing_data(instance, pricing_data)
		#add_stock_data(instance, stock_data)

		# Iterate through all data in validated_data and update the instance
		# with new values and save it.
		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		return instance

	def add_productdata_data(self, instance, validated_data):
		"""Handle the save, update and create of ProductData
		"""

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
		"""Handle the save, update and create of ProductImage
		"""
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
		"""Handle the save, update and create of Attribute and AttributeChoice
		"""

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

class ProductViewSet(viewsets.ModelViewSet):
	serializer_class = ProductSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Product.objects.all()
		parent = self.request.query_params.get('parent', None)
		if parent:
			queryset = queryset.filter(category=parent)

		return queryset

	def create(self, request, *args, **kwargs):
		# Add a slugify version of the `name` to the request and then
		# pass it to the Serializer.
		request.data['slug'] = slugify(request.data['name'])

		serialized = self.serializer_class(data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

	def update(self, request, pk=None):
		images = request.data.pop('productimage_set')

		# To see if the request contains existing images uploaded before, or new images that should
		# be uploaded now, we check if the image value is an URL (Existing images point to an URL).
		validator = URLValidator()
		for image in images:
			# If the validation passes, remove the `image` from the request, since it means the image
			# already exists and is not updated.
			try:
				validator(image['image'])
				image.pop('image')

			# If it fails validation, it means that the image contains a base64 string and we should
			# create a file out of the data and add it to our request.
			except ValidationError:
				img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", image['image']).groupdict()
				blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
				imagefile = StringIO(blob)
				imagefile = InMemoryUploadedFile(imagefile, None, image['filename'], 'image/jpeg', imagefile.len, None)
				image['image'] = imagefile

		request.data['productimage_set'] = images

		product = Product.objects.get(pk=pk)
		serialized = self.serializer_class(product, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response({'status': 'UPDATED', 'image_data': serialized.data})
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class CategoryViewSet(viewsets.ModelViewSet):
	serializer_class = CategorySerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Category.objects.all()

		parent = self.request.query_params.get('parent', None)
		if parent:
			queryset = queryset.filter(parent=parent)

		return queryset

	def create(self, request, *args, **kwargs):
		# Add a slugify version of the `name` to the request and then
		# pass it to the Serializer.
		request.data['slug'] = slugify(request.data['name'])

		serialized = self.serializer_class(data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

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
		depth = 1
		fields = (
			'id', 
			'date_created', 
			'voucher', 
			'carrier', 
			'currency', 
			'cartitem_set', 
			'total', 
		)

class CartViewSet(viewsets.ModelViewSet):
	queryset = Cart.objects.all()
	serializer_class = CartSerializer
	permission_classes = (IsAdminUser,)

class CustomFieldValueSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomFieldValue
		depth = 1
		exclude = ('id', 'order')

class OrderSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)
	cart = CartSerializer(read_only=True)
	customfieldvalue_set = CustomFieldValueSerializer(read_only=True, many=True)
	class Meta:
		model = Order
		depth = 1
		fields = (
			'id',
			'payment_status',
			'payment_option',
			'payment_reference', 
			'payment_id', 
			'date_created', 
			'cart', 
			'user', 
			'customfieldvalue_set', 
			'order_notification', 
		)

class OrderListSerializer(serializers.ModelSerializer):
	total = serializers.ReadOnlyField(source='get_total')
	class Meta:
		model = Order
		depth = 1
		fields = (
			'id',
			'date_created', 
			'user', 
			'total', 
		)

class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = (IsAdminUser,)

	def list(self, request):
		queryset = Order.objects.all().order_by('-pk')[:25]
		serializer = OrderListSerializer(queryset, many=True)
		return Response(serializer.data)

	def post(self, request, pk=None):
		return Response({'received_data': request.data})

	@detail_route(methods=['POST'])
	def add_notification(self, request, pk=None):
		note = Notification.objects.create(
			order=Order.objects.get(pk=pk), 
			notification_type=request.data['notification_type'], 
			note=request.data['note'], 
		)
		return Response({'received_data': request.data})

