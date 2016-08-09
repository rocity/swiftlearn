$(document).ready(function() {
    $('.owl-carousel').owlCarousel({
        loop: true,
        margin: 10,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            600: {
                items: 3,
                nav: false
            },
            1000: {
                items: 5,
                nav: false,
                loop: false
            }
        }
    });
    $('[data-toggle="popover"]').popover({
        html: true
    });



    $(document).on("change", "#tracker-type", function() {
        var text = $('.input-fixed input');
        if ($(this).val() == 'Hourly') {
            text.addClass('hidden');
        } else {
            text.removeClass('hidden');
        }
    });
    $('#profile-tab a').click(function(e) {
        e.preventDefault()
        $(this).tab('show')
    })

    $('#portfolio-modal').on('shown.bs.modal', function() {
        $('#myInput').focus()
    })
     $('upload-file input').change(function () {
    
    });
});
