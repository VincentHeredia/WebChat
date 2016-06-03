
//Tutorial for django web sockets: https://blog.heroku.com/archives/2016/3/17/in_deep_with_django_channels_the_future_of_real_time_apps_in_django
//Code example: https://github.com/jacobian/channels-example/blob/master/static/chat.js
//Heroku closes sockets automatically, 
//  reconnect solution used: https://github.com/joewalnes/reconnecting-websocket

$(function() {
	var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	var chatSocket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chatsocket/");
	var chatMessageCount = 0;
	
	chatSocket.onmessage = function(message){
		var data = JSON.parse(message.data);//get data
		var chatWindow = $("#chatEle");
		
		/* Format
		<div class="message">
			<div class="timeStamp">12:20</div>
			<div class="chatUserName">UserName:</div>
			<div class="chatMessage">This is a message</div>
		</div>
		*/
		
		var date = new Date();
		
		//build new element
		var newElement = $('<div class="message"></div>');
		newElement.append($('<div class="chatTime"></div>').text((date.getHours()%12) + ":" + date.getMinutes() + ":" + date.getSeconds() + ", "));
		newElement.append($('<div class="chatUserName"></div>').text("You: "));
		newElement.append($('<div class="chatMessage"></div>').text(data.message));
		
		chatWindow.append(newElement);
		$("#chatEle").scrollTop($("#chatEle")[0].scrollHeight);//auto scroll
		
		if(chatMessageCount > 50){//remove old messages
			$("#chatEle .message").first().remove();
		}
		else{
			chatMessageCount++;
		}
	};
	
	$("#submitMessage").click(function() {
		var message = {
			message: $("#inputMessage").val()
		};
		chatSocket.send(JSON.stringify(message));
		$("#inputMessage").val("");//clear value
		$("#inputMessage").focus();
	});
	
});