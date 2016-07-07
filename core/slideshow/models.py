from django.db import models

class Slideshow(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'slideshow'

class Slide(models.Model):
	slideshow = models.ForeignKey(Slideshow)
	image = models.ImageField(upload_to="slideshow")
	url = models.URLField(max_length=255, blank=True, null=True)
	alt = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return "Slideshow Item #%s" % self.id

	class Meta:
		app_label = 'slideshow'