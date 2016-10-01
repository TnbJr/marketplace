// var getAllArticles = function(){
//     $.get('/article/list', function(data){
//         var template = $('#list-articles-template').html();
//         var rendered = Mustache.render(template, data);
//         $('#center-main').html(rendered);
//     });
// };

function apply_form_field_error(fieldname, error) {
  console.log("this is the field name", fieldname);
    var fieldNameId = $("#id_" + fieldname);
    var errorMessage = error[0].message;
    console.log(fieldNameId, errorMessage);
    // container = $("#div_id_" + fieldname),
    error_msg = $("<span />").addClass("help-inline ajax-error").text(errorMessage);
    fieldNameId.addClass('jared');
    // container.addClass("error");
    error_msg.insertAfter(fieldNameId);
}

function clear_form_field_errors(form) {
  console.log("the clear form ran");
    $(".ajax-error", $(form)).remove();
    $(".error", $(form)).removeClass("error");
}



var setupPage = function(){
  console.log('cheout js working han')
    // var template = $('#article-form-template').html();
    // $('#order-review').append(template);
    // getAllArticles()
};

var create_post = function (form) {
    console.log("create post is working!"); // sanity check
    console.log(form.attr('action'));
    $.ajax({
        url : form.attr('action'), // the endpoint
        type : form.attr('method'), // http method
        data : form.serialize(), // data sent with the post request
        // handle a successful response

        beforeSend:function() { 
        console.log("beofre send");
        clear_form_field_errors(form);
      },
        success : function(data) {
          var formParentID = '#' + form.parent().attr('id');
          console.log(formParentID);
          $(form).fadeOut(300, function(){ 
            $(this).remove();
          
          var template = $('#address-confirm').html();
          var rendered = Mustache.render(template, data);
          $(formParentID).append(rendered);
          $('#checkout').show()

        // $('#center-main').html(rendered);
          });
            // $('#post-text').val(''); // remove the value from the input
            console.log("this shit is lit", rendered); 
            console.log("this is the data", data); // log the returned json to the console
            // another sanity check
            // console.log(data.form_errors)
        //     for (var key in data.form_errors) {
        //     console.log(key);
        //     // Check for proper key in dictionary
        //     // if (key in {first_name: 1, last_name: 1, gender: 1, sex: 1, phone: 1, }) {
                 
        //     //     // Get error message
        //     //     // error = data.result[key][0];
        //     //     // Find related field
        //     //     // field = $("#edit_form").find("#div_id_" + key)
        //     //     // Attach error message before it
        //     //     // field.before('<p class="errorField"><em></em>' + error + '</p>');
        //     // }
        // }
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
          console.log("there was a error");
          console.log("this is the errors", errors)
          var errors = $.parseJSON(xhr.responseText);
          var slime = $.parseJSON(errors.form_errors)
          $.each(slime, function(index, value){
            apply_form_field_error(index, value);
          })
          // console.log("data", data);
            // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
          // console.log(xhr.status + ": " + xhr.responseText);
          // console.log(errmsg); // provide a bit more info about the error to the console
          // console.log(err);
        }

    });
};



$(document).ready(function(){
    setupPage();
     $('#address-form').on('submit', function(event){
        event.preventDefault();
        console.log('ajax form submit is working ');
        console.log(this);
        var $form = $(this); 
        create_post($form);
    //     var $form = $(this);
    //     var formData = $form.serialize();

    //     $form[0].reset();
    //     $.post('/article/create',formData, function(responseData){
    //         getAllArticles();
    //     });
    // });

    // $('#center-main').on('click', 'a', function(event){
    //     event.preventDefault();
    //     var $a = $(this);
    //     var path = $a.attr('href');
    //     $.get(path, function(data){
    //         var template = $('#article-detail-template').html();
    //         var rendered = Mustache.render(template, data);
    //         $('#right-main').html(rendered);
    //     });
    // });
    // $('#right-main').on('submit', 'form', function(event){
    //     event.preventDefault();
    //     var $form = $(this);
    //     var path = $form.attr('action');
    //     var formData = $form.serialize();
    //     $.post(path, formData, function(data){
    //         $('a#'+data.slug).trigger('click');
    //     });
    });

});
