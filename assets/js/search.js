$(document).ready(function(){
    // can search on type and submit
    $('#search-form').on('submit keyup',function(){
            var url = '/search/';
            var txtval = $('#search').val();
            $.get(url,{q:txtval}).done(function(data){
                // get response and display to this division
                $('.item-container').html(data); 
            });
       return false;   
    })

});