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
def ws_connect(message):
	# get room name
	room = message.content['path'].strip("/")
	# save room
	message.channel_session['room'] = room
	# add user to room
	Group("chat-%s" % room).add(message.reply_channel)

#receive
@enforce_ordering(slight=True)
@channel_session
@channel_session_user
def ws_message(message):
	room = Room.objects.get(label='room1') #temp line
	data = json.loads(message['text'])
	msg = data['message'].strip()
	
	if len(msg) < 1:
		return #do nothing, message is blank
	
	print(message.user.is_authenticated())
	if message.user.is_authenticated():
		username = message.user.username
	else:
		return
	
	
	m = room.messages.create(handle=username, message=data['message'])
	
	#only hold 50 messages in the database
	#note: might be a better idea to make a custom save() function for the Message model
	if room.messages.count() > 50:
		#remove oldest date
		room.messages.order_by('timestamp').first().delete() #can also use [0] instead of first()
	
	Group("chat-%s" % message.channel_session['room']).send({
		"text": json.dumps(m.as_dict()),
	})


#disconnect
@enforce_ordering(slight=True)
@channel_session
def ws_disconnect(message):
	Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)


""" Old functions
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