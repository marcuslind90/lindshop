from django.contrib import admin
from lindshop.core.product.models import Product, ProductImage
from lindshop.core.category.models import Category
from lindshop.core.stock.models import Warehouse, Stock
from lindshop.core.pricing.models import Currency, Taxrule, Voucher, Pricing, Discount
from lindshop.core.order.models import Order, Notification, CustomField, CustomFieldValue
from lindshop.core.customer.models import CustomerProfile, Country, Address
from lindshop.core.cart.models import Cart, CartItem
from lindshop.core.shipping.models import Carrier, CarrierPricing
from lindshop.core.attribute.models import Attribute, AttributeChoice
from lindshop.core.menu.models import MenuItem, Menu

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Warehouse)
admin.site.register(Stock)
admin.site.register(Currency)
admin.site.register(Taxrule)
admin.site.register(Voucher)
admin.site.register(Pricing)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(CustomField)
admin.site.register(CustomFieldValue)
admin.site.register(CustomerProfile)
admin.site.register(Country)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Carrier)
admin.site.register(CarrierPricing)
admin.site.register(Discount)
admin.site.register(Attribute)
admin.site.register(AttributeChoice)
admin.site.register(Menu)
admin.site.register(MenuItem)