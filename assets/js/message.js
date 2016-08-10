$(function(){
    $('.form-messages').on('submit',function(e){
        e.preventDefault();
        var url = $(this).attr('action');
        var data = $(this).serialize();
        $.post(url, data).then(function(response){
            $('#result').prepend(response);
            
            $('.form-messages').trigger("reset");
            data = {}; 
        });
        return false;
    });

});

$(function () {
    $('.reply').on('click', function (e) {
        e.preventDefault();
        var parent = $(this).parent(); 

        var replyForm = parent.find('.comment-reply');
        replyForm.removeClass('hide');

        // submit/save reply
        replyForm.find('.btn').on('click', function () {
            var form = replyForm.find('.form-reply').serialize();
            var url = replyForm.find('.form-reply').attr('action');

            $.post(url, form).done(function (response) {
                $('#reply-list').append(response);
                $('.form-reply').trigger("reset");
                data = {};
            });
            return false;
        });
    });
});
