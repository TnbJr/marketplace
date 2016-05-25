	var showFlashMessage = function(message){
	var template = "<div class='container container-alert-flash'><div class='col-sm-3 col-sm-offset-8'><div class='alert alert-success alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'></span></button>" +  message + "</div></div></div>"
	$("#jquery-message").append(template);
	$(".container-alert-flash").fadeIn();
	setTimeout(function(){
		$(".container-alert-flash").fadeOut();
	}, 2500);
};