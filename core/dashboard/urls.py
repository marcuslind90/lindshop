from django.conf.urls import url, patterns
from django.contrib.auth.views import login, logout
from lindshop.core.dashboard import views

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'), 
	url(r'^subscriptions/$', views.subscriptions, name='subscriptions'), 
	url(r'^plans/$', views.plans, name='plans'), 
	url(r'^login/$', views.login_view, name='login'), 
	url(r'^logout/$', views.logout_view, name='logout'), 
	url(r'^order/(?P<id_order>[0-9]+)/$', views.order, name='order'), 
	url(r'^products/$', views.products, name='products'), 
	url(r'^product/(?P<id_product>[0-9]+)/$', views.product, name='product'), 
	url(r'^categories/$', views.categories, name='categories'), 
	url(r'^category/(?P<id_category>[0-9]+)/$', views.category, name='category'), 
]

# Ajax/Form Submit URL patterns
urlpatterns += [ 
	url(r'^check-payments/', views.check_payments, name='check-payments'), 
	url(r'^add-notification/', views.add_notification, name='add-notification'), 
]