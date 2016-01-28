from django.db import models
from django.dispatch import receiver
from django.conf import settings

class CustomerProfile(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	dog_name = models.CharField(max_length=100, blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	key = models.CharField(max_length=32, null=True, blank=True)

	def __unicode__(self):
		if self.user.email:
			return self.user.email
		else:
			return "%s %s" % (self.user.first_name, self.user.last_name)

	@property
	def full_name(self):
		return "%s %s" % (self.user.first_name, self.user.last_name)

	@receiver(models.signals.post_save)
	def generate_key(sender, instance, **kwargs):
		if sender is CustomerProfile:
			# If key is default value (Not set).
			if instance.key is None or instance.key == "":
				import uuid
				instance.key = uuid.uuid1().hex
				instance.save()

	class Meta:
		app_label = 'customer'

class Country(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(unique=True)
	default = models.BooleanField(default=False)

	def __unicode__(self):
		return self.slug

	class Meta:
		app_label = 'customer'

class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	address = models.CharField(max_length=128, blank=True, null=True)
	zipcode = models.CharField(max_length=10, blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	country = models.ForeignKey(Country, blank=True, null=True)

	class Meta:
		app_label = 'customer'