$(function(){
    $('#form-messages').on('submit',function(e){
        e.preventDefault();
        var url = $(this).attr('action');
        var data = $(this).serialize();
        $.post(url, data).then(function(response){
            $('#result').prepend(response);
            
            $('#form-messages').trigger("reset");
            data = {};
          
        });

        return false;
    });

});
