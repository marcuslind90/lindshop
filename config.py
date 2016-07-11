from django.conf import settings

# General Settings
google_analytics		= settings.LINDSHOP.get('google_analytics', None)
google_webmastertools	= settings.LINDSHOP.get('google_webmastertools', None)

# Shop General Settings
shop_name 				= settings.LINDSHOP.get('shop_name', 'Lindshop')
shop_logo 				= settings.LINDSHOP.get('shop_logo', None)
shop_base_template 		= settings.LINDSHOP.get('shop_base_template', 'lindshop/base.html')


# Cart Settings
cart_display_top		= settings.LINDSHOP.get('cart_display_top', True)
cart_editable_amount	= settings.LINDSHOP.get('cart_editable_amount', True)
cart_allow_delete		= settings.LINDSHOP.get('cart_allow_delete', True)

# Checkout Settings
checkout_show_vat		= settings.LINDSHOP.get('checkout_show_vat', True)
checkout_shipping_hide 	= settings.LINDSHOP.get('checkout_shipping_hide', False)
checkout_banktransfer	= settings.LINDSHOP.get('checkout_banktransfer', True)

# Subscription Settings
subscription_premium	= settings.LINDSHOP.get('subscription_premium', 100)

# Order settings
order_email_alert		= settings.LINDSHOP.get('order_email_alert', True)

# Admin settings
admin_emails 			= settings.LINDSHOP.get('admin_emails', [])

# Product Settings
products_per_row		= settings.LINDSHOP.get('products_per_row', 4)
products_per_row_mobile	= settings.LINDSHOP.get('products_per_row_mobile', 2)
product_thumbnail_width = settings.LINDSHOP.get('product_thumbnail_width', 260)
product_thumbnail_height= settings.LINDSHOP.get('product_thumbnail_height', 360)
product_thumbnail_size	= "%sx%s" % (product_thumbnail_width, product_thumbnail_height)
product_gallery_thumbnail_width = settings.LINDSHOP.get('product_gallery_thumbnail_width', 80)
product_gallery_thumbnail_height = settings.LINDSHOP.get('product_gallery_thumbnail_height', 80)
product_gallery_thumbnail_size = "%sx%s" % (product_gallery_thumbnail_width, product_gallery_thumbnail_height)

# Category Page Settings
category_add_to_cart	= settings.LINDSHOP.get('category_add_to_cart', False)
category_order_by		= settings.LINDSHOP.get('category_order_by', 'name')

subscription_payment	= settings.LINDSHOP.get('subscription_payment', None)