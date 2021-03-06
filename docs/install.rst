Installation
============

1. Install the application using :code:`pip` in the following way:

.. code-block:: python

   pip install lindshop

.. todo:: This is currently on the to-do list and will supported when the project go into Beta. Currently you have to manually download the source from Github and add it to your project.

2. Add all the mandatory applications to your :code:`INSTALLED_APPS` directory in the :code:`settings.py` file of your Django project.

.. code-block:: python

   INSTALLED_APPS = (
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'lindshop',                   # Required
       'lindshop.core.attribute',    # Required
       'lindshop.core.cart',         # Required
       'lindshop.core.category',     # Required
       'lindshop.core.checkout',     # Required
       'lindshop.core.customer',     # Required
       'lindshop.core.dashboard',    # Required
       'lindshop.core.order',        # Required
       'lindshop.core.payment',      # Required
       'lindshop.core.pricing',      # Required
       'lindshop.core.product',      # Required
       'lindshop.core.shipping',     # Required
       'lindshop.core.stock',        # Required
       'lindshop.core.subscription', # Required
       'lindshop.core.menu',         # Required
       'lindshop.core.breadcrumbs',  # Required
       'sorl.thumbnail',             # Required
       'rest_framework',             # Required
   )

3. Add URL routing to your projects main :code:`urls.py` file.

.. code-block:: python

   urlpatterns = [
       url(r'^admin/', include(admin.site.urls)),
       url(r'^', include('lindshop.urls', namespace="shop")),  # Required
   ]

4. To configure and change settings of your store, add a directory called :code:`LINDSHOP = {}` to your :code:`settings.py` file. All the settings relevant to the core functionality of Lindshop will go into this dictionary.

Import Demo Data
^^^^^^^^^^^^^^^^

There's a build in management command for importing demo data to your database if you want to demo and try out Lindshop.

.. code-block:: python

	python manage.py import_defaults

The command will import the following to your database:

* Categories
* Countries
* Currencies
* Tax rules
* Products
* Product Images
* Subscription Plans
* Prices
* Carriers
* Carrier Pricings
* Attributes (Color, Size etc) of products
* Attribute Choices (Red, Blue, Small, Large) of attributes


Configuring Your Store
======================

As we mentioned earlier, all settings related to the core functionality of Lindshop is set in your :code:`settings.py` file with the :code:`LINDSHOP = {}` directory.

Example of how to set the name of your store:

.. code-block:: python

   LINDSHOP = {
       'shop_name': 'My New Store', 
   }

Available Settings
^^^^^^^^^^^^^^^^^^

.. attribute:: google_analytics

   Your Google Analytics ID. This will automatically add the Google Analytics tracking code to your store.

   Type: String

   Default: None

.. attribute:: google_webmastertools

   Your Google Webmaster Tools meta tag ID. This will automatically add the Google Webmaster Tools meta tag to the <head> of your store.

   Type: String

   Default: None

.. attribute:: shop_name

   The name of your store, this is used in confirmation emails, titles and plenty of places on the site.

   Type: String

   Default: "Lindshop"

.. attribute:: shop_logo

   The URL to a logo of your store. This logo will be used in emails and in templates.

   Type: String

   Default: None

.. attribute:: shop_base_template

   The base template of your store. All templates will be extended from this base template. If you want to create your own base template we recommend you to copy the original base template and base your new template on that.

   Type: String

   Default: "lindshop/base.html"

.. attribute:: cart_display_top

   This settings controls if you want to display the dropdown cart on the top of the page at all times. 

   Type: Boolean

   Default: True

.. attribute:: cart_editable_amount

   Should the amount be editable in the dropdown cart. Setting this option to True displays all amounts in inputs that can be edited. False means that the amount is just printed as text.

   Type: Boolean

   Default: True

.. attribute:: cart_allow_delete

   Should the user be able to delete and remove products from the shopping cart. True displays a Trash/Delete icon while False remove the ability to do so.

   Type: Boolean

   Default: True

.. attribute:: checkout_show_vat

   Set if the VAT should be displayed in the summary of the Checkout page. False will hide VAT.

   Type: Boolean

   Default: True

.. attribute:: checkout_shipping_hide

   Set if you want to hide the shipping price in the summary of the Checkout page. True will hide the shipping information.

   Type: Boolean

   Default: False

.. attribute:: checkout_banktransfer

   Activates or Disables bank transfer as a payment option in the checkout.

   Type: Boolean

   Default: True

.. attribute:: subscription_premium

   Added price on subscriptions that choose Premium option (Upsell)

   Type: Integer

   Default: 100

.. attribute:: order_email_alert

   Should emails be send out to the administrators when a new order is created?

   Type: Boolean

   Default: True

.. attribute:: admin_emails

   List of administrator emails that should get order alerts.

   Type: List

   Default: []

.. attribute:: products_per_row

   Amount of products that should be displayed per row on category pages on large displays.

   Type: Integer

   Default: 4

.. attribute:: products_per_row_mobile

   Amount of products that should be displayed per row on category pages on mobile phones.

   Type: Integer

   Default: 2

.. attribute:: product_thumbnail_width

   The width in pixels of product thumbnails that are generated when a new product image is uploaded.

   Type: Integer

   Default: 260

.. attribute:: product_thumbnail_height

   The height in pixels of product thumbnails that are generated when a new product image is uploaded.

   Type: Integer

   Default: 360

.. attribute:: product_thumbnail_size

   The dimensions of product thumbnails. This setting is a string that combines the value of :code:`product_thumbnail_width` and :code:`product_thumbnail_height`.

   Type: String

   Default: "%sx%s" % (product_thumbnail_width, product_thumbnail_height)

.. attribute:: category_add_to_cart

   Should "Add to Cart" buttons be displayed under the products on the Category page, or should user be forced to go into the product page before they can add the product to the cart.

   Type: Boolean

   Default: False

.. attribute:: category_order_by

   The attribute that Categories should be ordered by in the category navigation list.

   Type: String
   
   Default: 'name'

.. attribute:: subscription_payment

   Set the class of the subscription payment module. Unlike the setting for normal payment modules where you can define a list of multiple different payment options, with subscription_payment you can only define a single payment option.

   The string is formated as :code:`lindshop-stripe.wrapper.StripeWrapper`.

   Type: String
   
   Default: None