from django.conf.urls import url

from . import views

app_name = 'chat'
urlpatterns = [
	# ex: /chat/
	url(r'^$', views.index, name='index'),
]