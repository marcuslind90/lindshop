from django.db import models
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.conf import settings

from lindshop import config
from datetime import date

class Order(models.Model):
	cart = models.ForeignKey('cart.Cart')
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	payment_status = models.CharField(max_length=20, default="unpaid", choices=(("paid", "Paid"), ("unpaid", "Unpaid")))
	payment_option = models.CharField(max_length=100, default="unknown")
	subscription_plan = models.ForeignKey('subscription.Plan', blank=True, null=True)
	subscription = models.BooleanField(default=False)
	subscription_status = models.CharField(max_length=20, choices=(("active", "Active"), ("unpaid", "Unpaid"), ("canceled", "Canceled")), null=True, blank=True)
	subscription_enddate = models.DateField(blank=True, null=True)
	payment_reference = models.CharField(max_length=200, blank=True, null=True)
	payment_id = models.CharField(max_length=200, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "#%s" % self.id

	@property
	def is_past_due(self):
		if self.subscription_enddate < date.today():
			return True
		else:
			return False

	def send_confirmation(self):
		subject = _('TailBay Order Confirmation')
		logo = config.shop_logo
		shop_name = config.shop_name
		cta_link = "http://tailbay.com/"
		# Load the Email Template and save the HTML as a string.
		msg_html = render_to_string('mail/order-confirmation.html', 
			{
				'subject': subject, 
				'logo': logo, 
				'shop_name': shop_name, 
				'cta_link': cta_link, 
				'cta_text': _('Go to TailBay'), 
				'order': self
			}
		)

		# Load the Text message. This is send as a backup together with the HTML message
		# for the users that can not see HTML emails.
		msg_text = render_to_string('mail/order-confirmation.txt', 
			{}
		)

		# Django's build in send_mail function. Settings set in settings.py
		send_mail(
			subject=subject, 
			message=msg_text, 
			from_email="info@tailbay.com", 
			recipient_list=[self.user.email], 
			html_message=msg_html
		)

	@receiver(models.signals.post_save)
	def send_alert(sender, instance, **kwargs):
		if sender is Order and kwargs['created']:
			if config.order_email_alert:
				subject = _('TailBay New Order #%(id_order)s') % ({'id_order': instance.pk})
				logo = config.shop_logo
				shop_name = config.shop_name
				cta_link = "http://tailbay.com/"
				# Load the Email Template and save the HTML as a string.
				msg_html = render_to_string('mail/order-alert.html', 
					{
						'subject': subject, 
						'logo': logo, 
						'shop_name': shop_name, 
						'cta_link': cta_link, 
						'cta_text': _('Go to TailBay'), 
						'order': instance
					}
				)

				# Load the Text message. This is send as a backup together with the HTML message
				# for the users that can not see HTML emails.
				msg_text = render_to_string('mail/order-alert.txt', 
					{}
				)

				# Django's build in send_mail function. Settings set in settings.py
				send_mail(
					subject=subject, 
					message=msg_text, 
					from_email="info@tailbay.com", 
					recipient_list=config.admin_emails, 
					html_message=msg_html
				)

	class Meta:
		app_label = 'order'

class Notification(models.Model):
	order 				= models.ForeignKey(Order)
	notification_type 	= models.CharField(max_length=20, choices=(("shipping", "Shipping"), ("note", "Note")))
	date_created		= models.DateTimeField(auto_now_add=True)
	note 				= models.TextField(blank=True, null=True)

	class Meta:
		app_label = 'order'