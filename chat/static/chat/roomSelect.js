
$(function() {
	$(".roomLink").click(function(){
		window.location.href = "/chat/room/" + this.id.substring(4,this.id.length);
	});
});
