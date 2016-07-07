from django.db import models

class Menu(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'menu'

class MenuItem(models.Model):
	menu = models.ForeignKey(Menu)
	item_type = models.CharField(max_length=50)
	object_id = models.IntegerField(blank=True, null=True)
	label = models.CharField(max_length=100, blank=True, null=True)
	url = models.URLField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return "Menu Item #%s" % self.id

	class Meta:
		app_label = 'menu'