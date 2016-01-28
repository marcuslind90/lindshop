from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model):
	name = models.CharField(max_length=100)
	parent = models.ForeignKey('self', null=True, blank=True)
	description = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to="category", blank=True, null=True)
	slug = models.SlugField(unique=True)

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:category', args=[self.slug])

	class Meta:
		app_label = 'category'