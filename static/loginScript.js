
$(function() {
	
	$("#submitName").click(function(){
		$("form").submit();
	});
	
	$("#wrapper").keydown(function(e) {
		if (e.keyCode == 13) {
			$("form").submit();
		}
	});
	
});
