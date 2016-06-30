import json
import re

from channels import Group
from channels.sessions import channel_session, enforce_ordering
from chat.models import Room
from django.http import HttpResponseRedirect
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

# connect
@enforce_ordering(slight=True)
@channel_session
@channel_session_user_from_http
def ws_connect(message):
	# get room name
	requestedRoom = message['path'].strip('/').split('/')
	
	# check if user can join the room # this should never be reached
	room = Room.objects.get(id=requestedRoom[1]) # temp line, get room from input
	userInRoom = room.whiteListUsers.filter(handle=message.user.username)
	if room.type == 'private' and userInRoom.count() == 0:
		return HttpResponseRedirect('/chat/invaliduser') #user is not apart of the room
	
	# save room
	message.channel_session['room'] = requestedRoom[1]
	# add user to room
	Group("chat-%s" % message.channel_session['room']).add(message.reply_channel)

#receive
@enforce_ordering(slight=True)
@channel_session
@channel_session_user
def ws_message(message):
	room = Room.objects.get(id=message.channel_session['room']) #temp line
	msg = json.loads(message['text'])['message'].strip()
	funct = json.loads(message['text'])['funct'].strip()
	
	if funct and message.user.is_superuser: #if this is not a chat message and user is an admin
		if funct == "delete":
			deleteId = json.loads(message['text'])['id'].strip()
			room.messages.get(id=deleteId).delete()
			deleteMsg = {
				"type": "deleteMsg",
				"id": deleteId,
			}
			Group("chat-%s" % message.channel_session['room']).send({
				"text": json.dumps(deleteMsg), # convert to string
			})
			return # no message to process, return
	else:
		return # do nothing, user is not an admin
	
	
	if len(msg) < 1:
		return #do nothing, message is blank
	
	if message.user.is_authenticated():
		m = room.messages.create(handle=message.user.username, message=msg)
	else:
		return
	
	#only hold 50 messages in the database
	#note: might be a better idea to make a custom save() function for the Message model
	if room.messages.count() > 50:
		#remove oldest date
		room.messages.order_by('timestamp').first().delete() #can also use [0] instead of first()
	
	userPriv = "normal"
	if message.user.is_superuser: # if the user is an admin, send "admin" value for extra options
		userPriv = "admin"
		
	newMsg = {"type": "newMsg"}
	newMsg.update(m.as_dict()) # get message as a dict
	newMsg.update({"user": userPriv}) # add "user" data
	Group("chat-%s" % message.channel_session['room']).send({
		"text": json.dumps(newMsg), # convert to string
	})


#disconnect
@enforce_ordering(slight=True)
@channel_session
def ws_disconnect(message):
	Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)


""" Old functions: works as direct chat with no database
def ws_message(message):
	data = json.loads(message['text'])
	
	Group("chat").send({
        "text": message.content['text'],
    })
	
#add user to user pool
def ws_add(message):
	Group("chat").add(message.reply_channel)
	

def ws_disconnect(message):
	Group("chat").discard(message.reply_channel)
"""