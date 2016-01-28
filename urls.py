from django.conf.urls import patterns, include, url
from lindshop import views
from lindshop.core.product.views import product
from lindshop.core.category.views import category
from lindshop.core.cart.views import ajax_cart
from lindshop.core.checkout.views import checkout, ajax_checkout, process_checkout, thank_you
from lindshop.core.payment.views import payment_webhook, get_form
from lindshop.core.subscription.views import subscription_cancel, subscription_change

app_name = 'lindshop'

urlpatterns = [
	url(r'^$', views.landing, name='index'), 
	url(r'^checkout/$', checkout, name="checkout"), 
	url(r'^thank-you/$', thank_you, name="thank_you"), 
	url(r'^terms-of-service/$', views.terms, name="terms"), 
	url(r'^contact/$', views.contact, name="contact"), 
	url(r'^faq/$', views.faq, name="faq"), 
	url(r'^subscription-change/$', subscription_change, name="subscription-change"), 
	url(r'^subscription-cancel/$', subscription_cancel, name="subscription-cancel"), 
	url(r'^dashboard/', include('lindshop.core.dashboard.urls', namespace="dashboard")), 
]

# Ajax/Form Submit URL patterns
urlpatterns += patterns('', 
	url(r'^ajax-cart/', ajax_cart, name='ajax-cart'), 
	url(r'^ajax-checkout/', ajax_checkout, name='ajax-checkout'), 
	url(r'^process-checkout/', process_checkout, name="process-checkout"),
	url(r'^payment-webhook/', payment_webhook, name="payment-webhook"), 
	url(r'^payment-get-form/', get_form, name="get-form"), 
)

#
urlpatterns += patterns('', 
	url(r'^(?P<id_product>[0-9]+)-(?P<slug>[a-z\-0-9]+)/$', product, name="product"), 
	url(r'^(?P<category_slug>[a-z0-9-]+)/$', category, name="category"), 
)