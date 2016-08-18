$(function () {
    //create feedback to selected event
    $(document).on('submit', '.form-feedback', function(e){
        e.preventDefault();
        var url = $(this).attr('action');
        var data = $(this).serialize();
        console.log("test");
        $.post(url, data).done(function(response){
            $('.form-feedback').trigger('reset');
        });
        return false;
    });
});