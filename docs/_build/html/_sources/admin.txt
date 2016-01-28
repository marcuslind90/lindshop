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