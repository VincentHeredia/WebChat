from django.shortcuts import render
from django.template import loader
from chat.models import Room
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from chat.forms import PostForm
import urllib 

# Create your views here.

# render list of rooms for a user to select
def roomList(request, urlOrigin=""):
	# if the user is not logged in, redirect to login screen
	if request.user.is_authenticated():
		username = request.user.username
	else:
		return HttpResponseRedirect('/login')
	
	# get all private and public rooms
	try:
		privRooms = Room.objects.filter(type='private')
	except Room.DoesNotExist:
		privRooms = None
	try:
		pubRooms = Room.objects.filter(type='public')
	except Room.DoesNotExist:
		pubRooms = None
	
	# render room selection page
	return render(request, 'chat/roomSelection.html', {
		'userName': request.user.username,
		'urlOrigin': urlOrigin,
		'privateRooms': privRooms,
		'publicRooms': pubRooms,
	})

# render the selected chat room
def chatRoom(request, num):
	# if the user is not logged in, redirect to login screen
	if request.user.is_authenticated():
		username = request.user.username
	else:
		return HttpResponseRedirect('/login')
	
	# get room from database
	roomId = num;
	room = Room.objects.get(id=roomId)
	
	# redirect if the user is not on the rooms whitelist/not a public room
	userInRoom = room.whiteListUsers.filter(handle=request.user.username)
	if room.type == 'private' and userInRoom.count() == 0:
		return HttpResponseRedirect('/chat/invaliduser') #user is not apart of the room
	
	# get messages
	messages = reversed(room.messages.order_by('-timestamp'))
	
	# find room admin
	userAdminName = room.roomAdmin
	if userAdminName == username:
		userAdmin = True
	else:
		userAdmin = False
	
	# render room page
	return render(request, 'chat/chatRoom.html', {
		'userName': username,
		'userAdmin': userAdmin,
		'roomId': roomId,
		'room': room,
		'messages': messages,
	})
	
# render the create room page
def createRoom(request):
	# if the user is not logged in, redirect to login screen
	if request.user.is_authenticated():
		username = request.user.username
	else:
		return HttpResponseRedirect('/login')
	
	c = {}
	c.update(csrf(request))
	
	# if this is a form submission 
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			roomName = form.cleaned_data['roomName']
			roomLabel = urllib.parse.quote_plus(roomName)
			roomType = form.cleaned_data['roomType']
			c['hasErrors'] = False
			if roomType == "none":
				c['typeError'] = True
				c['hasErrors'] = True
			if Room.objects.filter(name=roomName).count() > 0:
				c['uniqueError'] = True
				c['hasErrors'] = True
				
			if not c['hasErrors']:
				r = Room.objects.create(name=roomName, label=roomLabel, type=roomType, roomAdmin=username)
				r.whiteListUsers.create(handle=username)
				r.save()
				return HttpResponseRedirect('/chat/loggedin/')
		else:
			c['fieldError'] = True
			c['hasErrors'] = True
			
	form = PostForm()
	c['form'] = form
	c['userName'] = request.user.username
	
	return render(request, 'chat/createRoom.html', c)
	
	