Lindshop - An Ecommerce Platform For Django
============================================

**_This project is currently under development and not ready for production use. Please Star/Watch it for future updates._**

Introduction
------------

Lindshop is a Django application that handles all the basic features of an ecommerce websites such as Products, Carts, Orders, Payments and so on. Lindshop is made to be easy to extend and customize to the type of ecommerce website that you're looking to build, no matter if it's a normal store with a few categories and products, or if it's an online subscription service with a single product.

* Author: Marcus Lind (marcuslind90@gmail.com)
* Github: https://github.com/marcuslind90/lindshop
* Read-The-Docs: http://lindshop.readthedocs.org/en/latest/


Installation
------------

1. Install the application using `pip` in the following way:

```
   pip install lindshop
```

**_This is currently on the to-do list and will supported when the project go into Beta. Currently you have to manually download the source from Github and add it to your project._**

2. Add all the mandatory applications to your `INSTALLED_APPS` directory in the `settings.py` file of your Django project.

```
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
   )
```

3. Add URL routing to your projects main `urls.py` file.

```
   urlpatterns = [
       url(r'^admin/', include(admin.site.urls)),
       url(r'^', include('lindshop.urls', namespace="shop")),  # Required
   ]
```

4. To configure and change settings of your store, add a directory called `LINDSHOP = {}` to your `settings.py` file. All the settings relevant to the core functionality of Lindshop will go into this dictionary.

Import Demo Data
------------

There's a build in management command for importing demo data to your database if you want to demo and try out Lindshop.

```
	python manage.py import_defaults
```

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