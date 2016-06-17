
//Tutorial for django web sockets: https://blog.heroku.com/archives/2016/3/17/in_deep_with_django_channels_the_future_of_real_time_apps_in_django
//Code example: https://github.com/jacobian/channels-example/blob/master/static/chat.js
//Heroku closes sockets automatically, 
//  reconnect solution used: https://github.com/joewalnes/reconnecting-websocket

$(function() {
	var chatMessageCount = 0;//need to get number of messages
	var scrolledUp = false;
	
	$("#chatEle").scrollTop($("#chatEle")[0].scrollHeight);//auto scroll
	
	chatSocket.onmessage = function(message){
		var data = JSON.parse(message.data);//get data
		buildNewElement(data);
		chatMessageCount++;
	};
	
	//Submit button
	$("#submitMessage").click(function() {
		sendSocketMessage();
	});
	
	//Enter button
	$("#inputMessage").keydown(function(e) {
		if (e.keyCode == 13) {
			sendSocketMessage();
		}
	});
	
	//if user scrolls to the bottom
	$("#chatEle").scroll(function() {
		offset = $("#chatEle")[0].scrollHeight - $("#chatEle").height();
		if($("#chatEle").scrollTop() == offset) {
			scrolledUp = false;
		}
		else {
			scrolledUp = true;
		}
	});
	
	//send a message
	function sendSocketMessage(){
		var message = {
			message: $("#inputMessage").val()
		};
		chatSocket.send(JSON.stringify(message));
		$("#inputMessage").val("");//clear value
		$("#inputMessage").focus();
	}
	
	//builds a message element and inserts it into the chat window
	function buildNewElement(data) {
		var chatWindow = $("#chatEle");
		
		//build new element
		var newElement = $('<div class="message"></div>');
		newElement.append($('<div class="chatTime"></div>').html(data.timestamp + ",&nbsp;"));
		newElement.append($('<div class="chatUserName"></div>').html(data.handle + ":&nbsp;"));
		newElement.append($('<div class="chatMessage"></div>').html(data.message));
		
		chatWindow.append(newElement);
		
		if (!scrolledUp){
			$("#chatEle").scrollTop($("#chatEle")[0].scrollHeight);//auto scroll
		}
		
		if(chatMessageCount > 50){//remove old messages
			$("#chatEle .message").first().remove();
		}
	}
});
