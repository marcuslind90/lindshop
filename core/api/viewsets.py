from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

import re
from StringIO import StringIO

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

import lindshop.core.api.serializers as serializers
import lindshop.core.api.utils as utils

class CarrierViewSet(viewsets.ModelViewSet):
	"""The ViewSet of the Carrier object. This handles the request and
	sends it to the serializer.
	"""
	serializer_class = serializers.CarrierSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		return Carrier.objects.all()

	def create(self, request, pk=None):

		# If `logo` is included in the call, it means an Image is uploaded.
		# The image from AngularJS is stored as a  base64 string. We use the string and 
		# create an image of it and then replace the original base64 string stored in the request
		# with the new image.
		if 'logo' in request.data and request.data['logo'] is not None and request.data['logo'] != "":
			request.data['logo'] = utils.upload_image(request.data['filename'], request.data['logo'])

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
				request.data['logo'] = utils.upload_image(request.data['filename'], request.data['logo'])

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

class SlideshowViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.SlideshowSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		return Slideshow.objects.all()

	def create(self, request, pk=None):
		# Seperate nested data
		slides = request.data.pop('slide_set')

		# For each slide that is being created, we create a new file by using the base64 data send in the request
		# and then replace the original value with the new file.
		for slide in slides:
			slide['image'] = utils.upload_image(slide['filename'], slide['image'])

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
				slide['image'] = utils.upload_image(slide['filename'], slide['image'])

		request.data['slide_set'] = slides

		slideshow = Slideshow(pk=pk)
		serialized = self.serializer_class(slideshow, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response({'status': 'UPDATED', 'image_data': serialized.data})
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

class MenuViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.MenuSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		return Menu.objects.all()

class WarehouseViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.WarehouseSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		return Warehouse.objects.all()

class StockViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.StockSerializer
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

class AttributeViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.AttributeSerializer
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

class ProductImageViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.ProductImageSerializer
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
		request.data['image'] = utils.upload_image(request.data['filename'], request.data['image'])

		image = ProductImage(pk=pk)
		serialized = self.serializer_class(image, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data, status=status.HTTP_201_CREATED)
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

class CurrencyViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.CurrencySerializer
	queryset = Currency.objects.all()
	permission_classes = (IsAdminUser,)

class TaxruleViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.TaxruleSerializer
	queryset = Taxrule.objects.all()
	permission_classes = (IsAdminUser,)

class PricingViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.PricingSerializer
	permission_classes = (IsAdminUser,)

	def get_queryset(self):
		queryset = Pricing.objects.all()
		product = self.request.query_params.get('product', None)
		if product:
			queryset = queryset.filter(product=product)

		return queryset

class CountryViewSet(viewsets.ModelViewSet):
	queryset = Country.objects.all()
	serializer_class = serializers.CountrySerializer
	permission_classes = (IsAdminUser,)

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer
	permission_classes = (IsAdminUser,)

class ProductDataPresetViewSet(viewsets.ModelViewSet):
	queryset = ProductDataPreset.objects.all()
	serializer_class = serializers.ProductDataPresetSerializer
	permission_classes = (IsAdminUser,)

class ProductViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.ProductSerializer
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
				image['image'] = utils.upload_image(image['filename'], image['image'])

		request.data['productimage_set'] = images

		product = Product.objects.get(pk=pk)
		serialized = self.serializer_class(product, data=request.data)
		
		if serialized.is_valid():
			serialized.save()
			return Response({'status': 'UPDATED', 'image_data': serialized.data})
		else:
			return Response({'status': 'FAILED', 'errors': serialized.errors})

class CategoryViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.CategorySerializer
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

class CartViewSet(viewsets.ModelViewSet):
	queryset = Cart.objects.all()
	serializer_class = serializers.CartSerializer
	permission_classes = (IsAdminUser,)

class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = serializers.OrderSerializer
	permission_classes = (IsAdminUser,)

	def list(self, request):
		queryset = Order.objects.all().order_by('-pk')[:25]
		serializer = serializers.OrderListSerializer(queryset, many=True)
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
