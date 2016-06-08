from django.shortcuts import render
from django.template import loader
from chat.models import Room

# Create your views here.


def chatRoom(request):
	room = Room.objects.get(label='room1')#templine
	messages = reversed(room.messages.order_by('-timestamp'))
	
	return render(request, 'chat/chatRoom.html', {
		'room': room,
		'messages': messages,
	})