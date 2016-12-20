from django.conf.urls import url
from django.contrib.auth.views import login, logout
from lindshop.core.dashboard import views

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'), 
	url(r'^login/$', views.login_view, name='login'), 
	url(r'^logout/$', views.logout_view, name='logout'), 
]

# Ajax/Form Submit URL patterns
urlpatterns += [
	url(r'^add-notification/', views.add_notification, name='add-notification'), 
]