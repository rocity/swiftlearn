$(function() {
    // scroll messages to bottom
    $('#conversation-container').scrollTop($('#conversation-container')[0].scrollHeight);

    $(document).on('submit', '#message-form', function (e) {
        console.log('yohooo')
        e.preventDefault();

        var url = $(this).attr('action'),
            data = $(this).serialize();

        $.post(url, data).done(function (response) {

            console.log(data);

            data = {};
        })

        return false;
    })

});