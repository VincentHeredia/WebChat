import json

from channels import Group


def ws_message(message):
	data = json.loads(message['text'])
	print(data)
	
	Group("chat").send({
        "text": message.content['text'],
    })
	
	"""
	Group("chat").send({
		"timestamp": "Time",
		"handle": "Handle",
		"message": "Hello, This is a message, im making this very long for testing purposes. A very long message has to be a few sentences to make coherent sense. I still think this message needs a few more sentences inorder for it to be long enough. I hope that I spell all the words I wrote correctly.",
	})
	"""
	
#add user to user pool
def ws_add(message):
	Group("chat").add(message.reply_channel)
	

def ws_disconnect(message):
	Group("chat").discard(message.reply_channel)