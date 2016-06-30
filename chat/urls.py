from django.conf.urls import url

from . import views

app_name = 'chat'
urlpatterns = [
	# ex: /chat/
	url(r'^createroom/$', views.createRoom, name='createRoom'),
	url(r'^room/(?P<num>[0-9]+)/$', views.chatRoom, name='chatRoom'),
	url(r'^(?P<urlOrigin>[a-z]+)/$', views.roomList, name='roomList'),
]