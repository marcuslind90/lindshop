from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import detail_route
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from lindshop.core.order.models import Order, CustomFieldValue, Notification
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.product.models import Product, ProductImage
from lindshop.core.customer.models import Address
from lindshop.core.category.models import Category
from lindshop.core.pricing.models import Pricing, Taxrule, Currency
from lindshop.core.attribute.models import Attribute, AttributeChoice
from lindshop.core.stock.models import Warehouse, Stock

import json
import re
from StringIO import StringIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify

# REST API Url Patterns (Used by AngularJS)
# Serializers define the API representation.
class WarehouseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Warehouse
		fields = '__all__'

class WarehouseViewSet(viewsets.ModelViewSet):
	serializer_class = WarehouseSerializer

	def get_queryset(self):
		queryset = Warehouse.objects.all()

		return queryset

class StockSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'

class StockViewSet(viewsets.ModelViewSet):
	serializer_class = StockSerializer

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
		choice_data = validated_data.pop('attributechoice_set')
		attribute = Attribute(**validated_data)
		attribute.save()

		for choice in choice_data:
			choice_obj = AttributeChoice(attribute=attribute, **choice)
			choice_obj.save()

		return attribute

class AttributeViewSet(viewsets.ModelViewSet):
	serializer_class = AttributeSerializer

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

class ProductImageViewSet(viewsets.ModelViewSet):
	serializer_class = ProductImageSerializer

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
		"""
		The uploaded file is send as an encoded URL. We pull out the data from the URL and then
		replace the image field of the request-data with the pulled out data.
		"""
		img_dict = re.match("data:(?P<type>.*?);(?P<encoding>.*?),(?P<data>.*)", request.data['image']).groupdict()
		blob = img_dict['data'].decode(img_dict['encoding'], 'strict')
		image = StringIO(blob)
		image = InMemoryUploadedFile(image, None, request.data['filename'], 'image/jpeg', image.len, None)
		#print image
		#image = StringIO.open(blob)
		request.data['image'] = image

		image = ProductImage(pk=pk)
		serialized = self.serializer_class(image, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response({'status': 'UPDATED', 'image_data': serialized.data})
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

class CurrencySerializer(serializers.ModelSerializer):
	class Meta:
		model = Currency

class CurrencyViewSet(viewsets.ModelViewSet):
	serializer_class = CurrencySerializer
	queryset = Currency.objects.all()

class TaxruleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Taxrule

class TaxruleViewSet(viewsets.ModelViewSet):
	serializer_class = TaxruleSerializer
	queryset = Taxrule.objects.all()

class PricingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pricing

class PricingViewSet(viewsets.ModelViewSet):
	serializer_class = PricingSerializer

	def get_queryset(self):
		queryset = Pricing.objects.all()
		product = self.request.query_params.get('product', None)
		if product:
			queryset = queryset.filter(product=product)

		return queryset

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

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class ProductSerializer(serializers.ModelSerializer):
	attribute_set = AttributeSerializer(many=True)

	class Meta:
		model = Product
		depth = 0
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
		)

	def create(self, validated_data):
		if 'attribute_set' in validated_data:
			validated_data.pop('attribute_set')
		if 'pricing_set' in validated_data:
			validated_data.pop('pricing_set')
		if 'stock' in validated_data:
			validated_data.pop('stock')
		if 'productimage_set' in validated_data:
			validated_data.pop('productimage_set')

		categories_data = validated_data.pop('categories')

		product = Product.objects.create(**validated_data)

		for category in categories_data:
			product.categories.add(category)

		return product

	def update(self, instance, validated_data):
		attribute_data = validated_data.pop('attribute_set')
		attribute_ids = []

		# Iterate through all data in validated_data and update the instance
		# with new values and save it.
		for(key, value) in validated_data.items():
			setattr(instance, key, value)
		instance.save()

		# Handle nested attribute values.
		for attribute in attribute_data:
			if 'id' in attribute:
				attribute_instance = Attribute.objects.get(pk=attribute['id'])
				self.update_attribute(attribute_instance, attribute)
			else:
				attribute_instance = self.create_attribute(attribute, instance.pk)
			attribute_ids.append(attribute_instance.pk)

		# Delete all attributes that was not included in the request, 
		# meaning... They have been deleted.
		for attribute in instance.attribute_set.all():
			if attribute.id not in attribute_ids:
				attribute.delete()

		return instance

	def update_attribute(self, instance, validated_data):
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

	def create_attribute(self, validated_data, id_product):
		choice_data = validated_data.pop('attributechoice_set')

		product = Product.objects.get(pk=id_product)
		attribute = Attribute(**validated_data)
		attribute.save()

		for choice in choice_data:
			choice_obj = AttributeChoice(attribute=attribute, **choice)
			choice_obj.save()

		return attribute

class ProductViewSet(viewsets.ModelViewSet):
	serializer_class = ProductSerializer

	def get_queryset(self):
		queryset = Product.objects.all()
		parent = self.request.query_params.get('parent', None)
		if parent:
			queryset = queryset.filter(category=parent)

		return queryset

	def create(self, request, *args, **kwargs):
		# First we slugify our Product Name and add the slug parameter.
		request.data['slug'] = slugify(request.data['name'])

		serialized = self.serializer_class(data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response({'status': 'CREATED', 'id': serialized.data['id']})
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		depth = 1

class CategoryViewSet(viewsets.ModelViewSet):
	serializer_class = CategorySerializer

	def get_queryset(self):
		queryset = Category.objects.all()

		parent = self.request.query_params.get('parent', None)
		if parent:
			queryset = queryset.filter(parent=parent)

		return queryset

class CartItemSerializer(serializers.ModelSerializer):
	product = ProductSerializer(read_only=True)
	price = serializers.ReadOnlyField(source='get_total')
	class Meta:
		model = CartItem
		depth = 1
		fields = (
			'amount', 
			'product', 
			'plan', 
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
			'subscription', 
			'subscription_status', 
			'subscription_enddate', 
			'payment_reference', 
			'payment_id', 
			'date_created', 
			'cart', 
			'user', 
			'subscription_plan', 
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

