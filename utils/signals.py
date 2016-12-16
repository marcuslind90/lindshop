from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender='customer.Country')
@receiver(pre_save, sender='pricing.Currency')
@receiver(pre_save, sender='stock.Warehouse')
def remove_defaults(instance, **kwargs):
	"""If the instance is setting the `default` parameter to True, 
	all other objects of the same type is set to `default=False`.
	"""
	if(instance.default):
		type(instance).objects.all().update(default=False)