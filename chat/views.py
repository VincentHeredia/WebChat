from django.shortcuts import render
from django.template import loader
from chat.models import Room

# Create your views here.


def chatRoom(request):
	room = Room.objects.get(label='room1')#templine
	messages = reversed(room.messages.order_by('-timestamp'))
	
	if request.user.is_authenticated():
		username = request.user.username
	else:
		return HttpResponseRedirect('/login')
	
	return render(request, 'chat/chatRoom.html', {
		'userName': username,
		'room': room,
		'messages': messages,
	})