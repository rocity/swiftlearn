
$(function(){
       $('.btn').on('click',function(){
       var tutor = $(this).parent().find('.tutor').val()
       var student = $(this).parent().find('.student').val()
       if(student){
        window.location.href = "/signup/?t="+student;
       }else{
        window.location.href = "/signup/?t="+tutor;
       }
    });

});
