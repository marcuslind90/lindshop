import csv
import os
from django.core.files.base import ContentFile
from django.apps import apps
from django.conf import settings


from lindshop.core.customer.models import Country
from lindshop.core.cart.models import Cart
from lindshop.core.category.models import Category
from lindshop.core.product.models import Product
from lindshop.core.pricing.models import Currency, Taxrule
from lindshop.core.shipping.models import Carrier
from lindshop.core.attribute.models import Attribute

class CSVImporter(object):

	def __init__(self, filename, delimiter=';'):
		self.filename = filename
		self.delimiter = delimiter

		self.models = {
			'user': apps.get_model(settings.AUTH_USER_MODEL), 
			'category': Category, # --
			'cart': Cart, 
			'parent': Category, # Need duplicate Category to handle Category recursive relation "Parent"
			'product': Product, 
			'currency': Currency, 
			'taxrule': Taxrule, 
			'carrier': Carrier, 
			'attribute': Attribute, 
			'country': Country
		}

	def csv_to_model(self, model):
		image = None  # Set to None as default.

		with open(self.filename, 'rb') as csvfile:
			csv_reader = csv.DictReader(csvfile, delimiter=self.delimiter)
			for row in csv_reader:
				for k, v in row.iteritems():
					if v is not None and len(v) > 0:
						if v[0] == '@':
							try:
								row[k] = self.models[k].objects.get(pk=int(v[1:]))
							except self.models[k].DoesNotExist:  # If does not exist, then get all the objects and return the first one.
								list_row = self.models[k].objects.all()
								row[k] = list_row[0]
							except Exception as ex:
								print "Model '%s' with Primary Key '%s' Error: %s" % (k, v, ex.message)
						elif v == 'False':
							row[k] = False
						elif v == 'True':
							row[k] = True
						elif any(string in v for string in ['.jpg', '.jpeg', '.png']):
							image = {'key': k, 'value': v}
					else:
						row[k] = None

				instance = model(**row)  # Create an instance of the model

				if image is not None:
					with open(image['value'], 'rb') as f:
  						data = f.read()

					instance.image.save(image['value'], ContentFile(data))

				instance.save()
