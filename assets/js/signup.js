$('#signup-options button').on("click", function() {
    var signup = $('.email-entry');
    var options = $('#signup-options');
    
    if ($(this).val() == 'email') {
        
        signup.removeClass('hidden');
        options.addClass('hidden');

    } else {
        signup.addClass('hidden');
    }
});

$(document).ready(function(){
    $('#signup').on('submit',function(event){
    // reset the validation before execute again
    clearValidation();
    // form execution
    var url = $(this).attr('action');
    var data  = $('#signup').serialize();

    $.post( url, data, function(response){

        if(response == "success"){
            window.location.href = "/user_category";
        }
    }).fail(function(response){
        var errors = JSON.parse(response.responseText);
        $.each(errors, function(index, error){

            var id = "#"+index+"_group";
            $(id).addClass('has-error');
            $(id).prepend('<p class="error">'+error+'</p>').css({"color":"#a94442"});

            var txtid = "#id_"+index;
            $(txtid).focus();
        });
    });

        event.preventDefault();
    });
});

function clearValidation(){
  $('.form-group').removeClass('has-error');
  $('.error').remove();
}