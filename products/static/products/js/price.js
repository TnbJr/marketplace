function updateCartItemCount(){
	var badge = $("#cart-count");
	$.ajax({
		type: "GET",
		url: "/cart/count",
		success: function(data){
			badge.text(data.count);
		},
		error: function(reponse, error){
			// console.log(error);
			console.log(reponse.responseText);
		}
	});

};

$(document).ready(function(){
	updateCartItemCount()

});