import json

from channels import Group
from channels.sessions import channel_session
from chat.models import Room

# connect
@channel_session
def ws_connect(message):
	# get room name
	room = message.content['path'].strip("/")
	
	# save room
	message.channel_session['room'] = room
	
	# add user to room
	Group("chat-%s" % room).add(message.reply_channel)
	

#receive
@channel_session
def ws_message(message):
	
	room = Room.objects.get(label='room1') #temp line
	data = json.loads(message['text'])
	m = room.messages.create(handle=data['user'], message=data['message'])
	
	print(message['text'])
	print("User " + data['user'])
	print("Message " + data['message'])
	print(m.as_dict())
	
	Group("chat-%s" % message.channel_session['room']).send({
		"text": json.dumps(m.as_dict()),
	})


#disconnect
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