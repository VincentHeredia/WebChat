from django.conf.urls import urls

from . import views

app_name = 'chat'
urlpatterns = [
	# ex: /chat/
	url(r'^$', views.IndexView.as_view(), name='index'),
]