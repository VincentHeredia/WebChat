

$(function() {
	/* needs to be updated
	$("#submitName").click(function(){
		var name = $("#inputName").val().trim();
		var pass = $("#inputPassword").val();
		var passCon = $("#inputConfirmPassword").val();
		
		var pat = new RegExp("^[a-zA-Z0-9]*$");
		var errorMessage = "";
		var hasError = false;
		
		if (name.length > 15){
			errorMessage += "Name is too long (max 12 characters)<br>";
			hasError = true;
		}
		if(name.length < 4){
			errorMessage += "Name is too short (min 4 characters)<br>";
			hasError = true;
		}
		if(!pat.test(name)){
			errorMessage += "Name cannot contain special characters<br>";
			hasError = true;
		}
		
		if(pass != passCon){
			errorMessage += "Passwords do not match<br>";
			hasError = true;
		}
		if(pass.length < 4){
			errorMessage += "Password is too short (min 5 characters)<br>";
			hasError = true;
		}
		if(pass.length > 30){
			errorMessage += "Password is too long (max 30 characters)<br>";
			hasError = true;
		}
		
		
		if(!hasError){
			$("form").submit();
		}
		else {
			$("#loginError").html(errorMessage);
		}
	});
	*/
});
