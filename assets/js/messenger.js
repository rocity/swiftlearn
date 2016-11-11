$(function() {
    // scroll messages to bottom
    $('#conversation-container').scrollTop($('#conversation-container')[0].scrollHeight);

    $(document).on('submit', '#message-form', function (e) {
        e.preventDefault();

        var url = $(this).attr('action'),
            data = $(this).serialize();

        $.post(url, data).done(function (response) {

            $('#conversation-container ul').append(response);
            $('#conversation-container').scrollTop($('#conversation-container')[0].scrollHeight);

            // $('#message-form input').val('');
            data = {};
        })

        $('#message-form input').val('');

        return false;
    })

});