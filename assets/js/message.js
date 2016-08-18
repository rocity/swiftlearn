$(function () {
    //create comment to selected event
    $(document).on('submit', '.form-comments', function(e){
        e.preventDefault();
        var url = $(this).attr('action');
        var data = $(this).serialize();
        $.post(url, data).done(function(response){
            $('#result').prepend(response);
            location.reload();
            $('.form-comments').trigger("reset");
            data = {};
        });
        return false;
    });

    //reply to a comment
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
                parent.find('.reply-list').append(response);
                location.reload();
                $('.form-reply').trigger("reset");
                data = {};
            });
            return false;
        });
    });

});
