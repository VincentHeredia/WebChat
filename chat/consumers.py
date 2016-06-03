import json

from channels import Group
from channels.sessions import channel_session


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
	Group("chat-%s" % message.channel_session['room']).send({
		"text": message.content['text'],
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