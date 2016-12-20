Lindshop - An Ecommerce Platform For Django
============================================

**_This project is currently under development and not ready for production use. Please Star/Watch it for future updates._**

Version: 0.0.1

Introduction
------------

Lindshop is a Django application that handles all the basic features of an ecommerce websites such as Products, Carts, Orders, Payments and so on. Lindshop is made to be easy to extend and customize to the type of ecommerce website that you're looking to build.

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
To add Lindshop to your project just navigate to it and run `git clone https://github.com/marcuslind90/lindshop`.

2. Add all the mandatory applications to your `INSTALLED_APPS` directory in the `settings.py` file of your Django project.

```
   INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'lindshop', # REQUIRED
        'lindshop.core.attribute',  # REQUIRED
        'lindshop.core.cart',       # REQUIRED
        'lindshop.core.category',   # REQUIRED
        'lindshop.core.checkout',   # REQUIRED
        'lindshop.core.customer',   # REQUIRED
        'lindshop.core.dashboard',  # REQUIRED
        'lindshop.core.order',      # REQUIRED
        'lindshop.core.payment',    # REQUIRED
        'lindshop.core.pricing',    # REQUIRED
        'lindshop.core.product',    # REQUIRED
        'lindshop.core.shipping',   # REQUIRED
        'lindshop.core.stock',      # REQUIRED
        'lindshop.core.menu',       # REQUIRED
        'lindshop.core.breadcrumbs',  # REQUIRED
        'lindshop.core.slideshow',  # REQUIRED
        'sorl.thumbnail',           # REQUIRED
        'rest_framework',           # REQUIRED
   )
```

3. To be able to handle overrides of Templates in Lindshop you need to import the `LINDSHOP_TEMPLATE_DIR` and add it to your `DIRS[]` in the `TEMPLATES` directory of your `settings.py` file. You also need to add the `shop_processor` to your `context_processors` setting. The `shop_processor` makes sure that all your Lindshop Settings are always included in every context of your shop.

```
    from lindshop import LINDSHOP_TEMPLATE_DIR
    location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', x)

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'templates'), # Required
                LINDSHOP_TEMPLATE_DIR # Required
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'lindshop.utils.context_processors.shop_processor', # Required
                ],
            },
        },
    ]
```

4. You also need to add `LINDSHOP = {}` and `LINDSHOP_PAYMENTS = {}` to your `settings.py` file that will handle any configuration of your store.

5. Add URL routing to your projects main `urls.py` file. Remember that you need to import the Django `include` function.

```
   from django.conf.urls import include
   urlpatterns = [
       url(r'^admin/', include(admin.site.urls)),
       url(r'^', include('lindshop.urls', namespace="shop")),  # Required
   ]
```

6. Run `python manage.py migrate` to generate the MySQL Database and all required tables.

7. You should now be able to run `python manage.py runserver` and visit your store and see an empty store front.

Access Dashboard
------------

You can access Lindshop's custom dashboard by navigating to `/dashboard/` when you're running your website. Any Django admin user can login to this dashboard.

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
* Prices
* Carriers
* Carrier Pricings
* Attributes (Color, Size etc) of products
* Attribute Choices (Red, Blue, Small, Large) of attributes