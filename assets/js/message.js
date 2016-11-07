$(function () {
    //create comment to selected event
    $(document).on('submit', '.form-comments', function(e){
        e.preventDefault();
        var url = $(this).attr('action');
        var data = $(this).serialize();
        $.post(url, data).done(function(response){
            $('#result').prepend(response);
            // console.log(response);
            // location.reload();
            var resp = returnhtml(response);
            $('#result').prepend(resp);
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

    function returnhtml(data) {
        var content = '<div class="content">' +
            '<a href="#" class="pull-right close"><i class="fa fa-times" aria-hidden="true"></i></a>' +
            '<a href="#" class="author">' + data.full_name + '</a>' +
            '<div class="metadata">' +
            '<span class="date">' + data.comment_date + '</span>' +
            '</div>' +
            '<div class="text">' +
            '<p>' + data.comment + '</p>' +
            '</div></div>',
            avatar = '<a href="#" class="avatar"><img src=""></a>',
            commentDiv = '<div class="comment">' + avatar + content + '</div>',
            commentSection = '<div class="event-content comment-section">' + commentDiv + '</div>';

        return commentSection;
    }

});
