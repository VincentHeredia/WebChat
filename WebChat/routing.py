from channels.routing import route
from chat.consumers import ws_message, ws_connect, ws_disconnect

channel_routing = [
	route("websocket.connect", ws_connect),
	route("websocket.disconnect", ws_disconnect),
	route("websocket.receive", ws_message),
]