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
	room = 'room1' #temp line, change to get a specific room in the database
	# save room
	message.channel_session['room'] = room
	# add user to room
	Group("chat-%s" % room).add(message.reply_channel)

#receive
@enforce_ordering(slight=True)
@channel_session
@channel_session_user
def ws_message(message):
	room = Room.objects.get(label=message.channel_session['room']) #temp line
	msg = json.loads(message['text'])['message'].strip()
	
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
	
	Group("chat-%s" % message.channel_session['room']).send({
		"text": json.dumps(m.as_dict()),
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