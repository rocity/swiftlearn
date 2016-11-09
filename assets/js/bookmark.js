$(function () {
    // catch event of clicking the bookmark icon
    $(document)
        .on('click', '.bookmark-event-icon-o', function (e) {
            e.preventDefault();

            var t = $(this),
                form = t.parent('.bookmark-event');

            form.submit();

        })
        .on('click', '.bookmark-event-icon', function (e) {
            e.preventDefault();

            var t = $(this),
                form = t.parent('.unbookmark-event');

            form.submit();

        });

    // Add event to user bookmarks
    $(document)
        .on('submit', '.unbookmark-event', function (e) {
            e.preventDefault();

            var t = $(this),
                url = t.attr('action'),
                data = t.serialize(),
                icon = t.find('i.fa-bookmark');

            $.post(url, data).done(function (response) {
                if (typeof response !== 'undefined') {
                    icon.addClass('fa-bookmark-o').removeClass('fa-bookmark');
                }
            })

            return false;
        })
        .on('submit', '.bookmark-event', function (e) {
            e.preventDefault();

            var t = $(this),
                url = t.attr('action'),
                data = t.serialize(),
                icon = t.find('i.fa-bookmark-o');

            $.post(url, data).done(function (response) {
                if (typeof response !== 'undefined') {
                    icon.addClass('fa-bookmark').removeClass('fa-bookmark-o');
                }
            })

            return false;
        });
});
