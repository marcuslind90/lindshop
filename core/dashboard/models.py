from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _


class AdminUser(models.Model):
	email = models.EmailField(unique=True, max_length=100)
	

	def __unicode__(self):
		return "#%s" % self.id

	class Meta:
		app_label = 'dashboard'