from django.conf.urls import patterns, include, url
from lindshop import views
from lindshop.core.product.views import product
from lindshop.core.category.views import category
from lindshop.core.cart.views import ajax_cart
from lindshop.core.checkout.views import checkout, ajax_checkout, process_checkout, thank_you
from lindshop.core.payment.views import payment_webhook, get_form
from lindshop.core.subscription.views import subscription_cancel, subscription_change
from lindshop.core.dashboard.api import UserViewSet, OrderViewSet, CartViewSet, ProductViewSet, CategoryViewSet, PricingViewSet, TaxruleViewSet, CurrencyViewSet, ProductImageViewSet, AttributeViewSet, StockViewSet, WarehouseViewSet, MenuViewSet, SlideshowViewSet, ProductDataPresetViewSet, CountryViewSet, CarrierViewSet
from rest_framework import routers

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
urlpatterns += [ 
	url(r'^ajax-cart/', ajax_cart, name='ajax-cart'), 
	url(r'^ajax-checkout/', ajax_checkout, name='ajax-checkout'), 
	url(r'^process-checkout/', process_checkout, name="process-checkout"),
	url(r'^payment-webhook/', payment_webhook, name="payment-webhook"), 
	url(r'^payment-get-form/', get_form, name="get-form"), 
]

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, base_name="User")
router.register(r'orders', OrderViewSet, base_name="Order")
router.register(r'carts', CartViewSet, base_name="Cart")
router.register(r'products', ProductViewSet, base_name="Product")
router.register(r'categories', CategoryViewSet, base_name="Category")
router.register(r'pricings', PricingViewSet, base_name="Pricing")
router.register(r'taxrules', TaxruleViewSet, base_name="Taxrule")
router.register(r'currencies', CurrencyViewSet, base_name="Currency")
router.register(r'images', ProductImageViewSet, base_name="ProductImage")
router.register(r'attributes', AttributeViewSet, base_name="Attribute")
router.register(r'warehouses', WarehouseViewSet, base_name="Warehouse")
router.register(r'stock', StockViewSet, base_name="Stock")
router.register(r'menus', MenuViewSet, base_name="Menu")
router.register(r'slideshows', SlideshowViewSet, base_name="Slideshow")
router.register(r'productdatapresets', ProductDataPresetViewSet, base_name="DataPreset")
router.register(r'countries', CountryViewSet, base_name="Country")
router.register(r'carriers', CarrierViewSet, base_name="Carrier")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [ 
	url(r'^api/', include(router.urls, namespace="api")),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Product and Category URLS
urlpatterns += [ 
	url(r'^(?P<id_product>[0-9]+)-(?P<slug>[a-z\-0-9]+)/$', product, name="product"), 
	url(r'^(?P<category_slug>[a-z0-9-]+)/$', category, name="category"), 
]