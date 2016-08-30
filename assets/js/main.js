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


    $('#setting-nav a').click(function(e) {
        e.preventDefault();
        $(this).tab('show');
        $('#setting-nav a').removeClass('active');
        $(this).addClass('active');
    });

    $('#portfolio-modal').on('shown.bs.modal', function() {
        $('#myInput').focus();
    });
});

$(function(){
    $('#btn-change-password').on('click',function(){
        resetValidation();
        var form =  $('#form_password_change');
        var url = form.attr('action')
        $.post(url,form.serialize()).done(function(response){
        var success = $('#success').prepend('Successfully added!');
        success.addClass('alert alert-success')
        form[0].reset();
        $('#changes-password').modal('hide');
        })
        .fail(function(response){
            var res = JSON.parse(response.responseText);
            $.each(res, function(index, content){
              var id = '#'+index+'_error';
              $(id).addClass('alert alert-danger');
              $(id).prepend(content);
              $('ul').css({'list-style':'None','padding':'0','margin':'0'});
            });
        });
    });
});
function resetValidation(){
    $('ul').remove();
    $('.error').removeClass('alert alert-danger');
}

$(function(){
  $('#password-changes').on('click',function(){
    resetValidation();
    });
});
