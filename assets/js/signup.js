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

    $.ajax({
            url:url,
            data:data,
            type:"POST",
            dataType:'json',
            error:function(response){
                var errors = JSON.parse(response.responseText);
                $.each(errors,function(index, error){
                     // error dissemination 
                     var id = "#"+index+"_group";
                        $(id).addClass('has-error');
                        $(id).prepend(error).css({"color": "#a94442"});
                        $('.errorlist').css({"list-style":"none","margin":"0","padding":"0"});
                    // set focus text field if there is a error
                     var txtid="#id_"+index;
                        $(txtid).focus();
                });
            }
    }).done(function(response){
        // success 
        if(response == "success"){
              window.location.href="/dashboard/";  
        }
      });
        event.preventDefault();
    });
});

function clearValidation(){
  $('.form-group').removeClass('has-error');
  $('.errorlist').remove();
}