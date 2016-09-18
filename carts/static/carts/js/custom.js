$(document).ready(function(){
 
 	console.log('cart js is working');
 	
 	'use strict'
	$('#black-button').on('click', function(event){
		event.preventDefault();
		$.ajax({
			url: "http://127.0.0.1:8000/carts/checkout",
			dataType: "json",
			success: function(data){
				console.log(data)
				var template = $("#list").html();
				var renderM = Mustache.render(template,data);
				$("#card-black").html(renderM)
				// console.log(template)
			}
		});
	});

	$('#white-button').on('click', function(event){
		event.preventDefault();
		$.ajax({
			url: "http://127.0.0.1:8000/whitecards",
			dataType: "json",
			success: function(data){
				console.log(data)
				var template = $("#list2").html();
				var renderM = Mustache.render(template, data);
				$("#card-white").html(renderM)
				// console.log(template)
			}
		});
	});
});
