from django.conf.urls import include, url
from lindshop import views
from lindshop.core.product.views import product
from lindshop.core.category.views import category
from lindshop.core.cart.views import ajax_cart
from lindshop.core.checkout.views import checkout, ajax_checkout, process_checkout, thank_you
from lindshop.core.payment.views import payment_webhook, get_form
from lindshop.core.dashboard.api import UserViewSet, OrderViewSet, CartViewSet, ProductViewSet, CategoryViewSet, PricingViewSet, TaxruleViewSet, CurrencyViewSet, ProductImageViewSet, AttributeViewSet, StockViewSet, WarehouseViewSet, MenuViewSet, SlideshowViewSet, ProductDataPresetViewSet, CountryViewSet, CarrierViewSet
import lindshop.core.api.viewsets as viewsets
from rest_framework import routers

app_name = 'lindshop'

urlpatterns = [
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
router.register(r'addresses', viewsets.AddressViewSet, base_name="Address")
router.register(r'users', viewsets.UserViewSet, base_name="User")
router.register(r'orders', viewsets.OrderViewSet, base_name="Order")
router.register(r'carts', viewsets.CartViewSet, base_name="Cart")
router.register(r'products', viewsets.ProductViewSet, base_name="Product")
router.register(r'categories', viewsets.CategoryViewSet, base_name="Category")
router.register(r'pricings', viewsets.PricingViewSet, base_name="Pricing")
router.register(r'taxrules', viewsets.TaxruleViewSet, base_name="Taxrule")
router.register(r'currencies', viewsets.CurrencyViewSet, base_name="Currency")
router.register(r'vouchers', viewsets.VoucherViewSet, base_name="Voucher")
router.register(r'images', viewsets.ProductImageViewSet, base_name="ProductImage")
router.register(r'attributes', viewsets.AttributeViewSet, base_name="Attribute")
router.register(r'warehouses', viewsets.WarehouseViewSet, base_name="Warehouse")
router.register(r'stock', viewsets.StockViewSet, base_name="Stock")
router.register(r'menus', viewsets.MenuViewSet, base_name="Menu")
router.register(r'slideshows', viewsets.SlideshowViewSet, base_name="Slideshow")
router.register(r'productdatapresets', viewsets.ProductDataPresetViewSet, base_name="DataPreset")
router.register(r'countries', viewsets.CountryViewSet, base_name="Country")
router.register(r'carriers', viewsets.CarrierViewSet, base_name="Carrier")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [ 
	url(r'^api/', include(router.urls, namespace="api")),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]