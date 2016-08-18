Administration and Dashboard
============================

Management Dashboard
^^^^^^^^^^^^^^^^^^^^

Instead of using the default Django admin backend, Lindshop has its own backend where administrators can manage their store. To login to the Lindshop backend you have to visit :code:`/dashboard/` of your site's URL.

Create Dashboard Administrator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lindshop is using Django's default User Model to handle backend users that can manage the store. Add a Django Super User to get an account to login with.

.. code-block:: python

   python manage.py createsuperuser


Errors
^^^^^^

.. code-block:: javascript

   “No 'Access-Control-Allow-Origin' header is present on the requested resource”

If you get the following error it probably is because you are using a third party storage for your 
static files such as Amazon S3. This means that your dashboard AngularJS template files are now stored remotely and to access them AngularJS need to do CORS calls to get the template files.

You solve this error by allowing CORS calls to your storage.