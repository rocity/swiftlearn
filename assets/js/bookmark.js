$(function () {
    // Add event to user bookmarks
    $(document).on('submit', '.bookmark-event', function (e) {
        e.preventDefault();

        var t = $(this),
            url = t.attr('action'),
            data = t.serialize();

        $.post(url, data).done(function (response) {
            console.log('bookmarked');
            console.log(response);
        })

        return false;
    });
});
