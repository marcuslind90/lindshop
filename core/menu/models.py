from django.db import models

class MenuItem(models.Model):
	custom_label = models.CharField(max_length=100, blank=True, null=True)
	category = models.ForeignKey('category.Category', blank=True, null=True)
	custom_url = models.URLField(max_length=200, blank=True, null=True)

	def __unicode__(self):
		if self.label:
			return self.label
		elif self.category:
			return self.category.name
		else:
			return self.id

	@property
	def label(self):
		if self.custom_label:
			return self.custom_label
		elif self.category:
			return self.category.name
		else:
			return "None"

	@property
	def url(self):
		if self.custom_url:
			return self.custom_url
		elif self.category:
			return self.category.get_absolute_url
		else:
			return "None"

	class Meta:
		app_label = 'menu'

class Menu(models.Model):
	name = models.CharField(max_length=100)
	items = models.ManyToManyField(MenuItem)
	slug = models.SlugField(unique=True)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'menu'

