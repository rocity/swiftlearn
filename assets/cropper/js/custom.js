$(function() {
  var fileuploader = $('#fileupload');
  var defaultimg = $('.image_default').val(); 
  $('.image-editor').cropit({
    exportZoom:.5,
    imageBackground: true,
    imageBackgroundBorderWidth: 20,
    imageState: {
      src: defaultimg,
    },
    onImageError: function(e) {
            if (e.code === 1) {
                $('.error-msg').text("Please use an image that's at least " + $('.cropit-preview').outerWidth() + "px in width and " + $('.cropit-preview').outerHeight() + "px in height.");
                $('.cropit-preview').addClass("has-error")
                    window.setTimeout(function() {
                        return function() {
                            return $('.cropit-preview').removeClass("has-error")
                        }
                    }(this), 3e3)
            }
        }

  });

 // disabled button
  $('#btn_ccw').prop('disabled', true);
  $('#btn_cw').prop('disabled', true);
  $('#btn_submit').prop('disabled', true);

  $('#zooming').prop('disabled', true);

  $('.rotate-cw').click(function() {
    $('.image-editor').cropit('rotateCW');
  });
  $('.rotate-ccw').click(function() {
    $('.image-editor').cropit('rotateCCW');
  });

  $('#btn_submit').on('click',function(){
      var imageData = $('.image-editor').cropit('export');
        $('.profile_picture').val(imageData);

      var imagename = fileuploader.val().replace(/C:\\fakepath\\/i, '');
        $('.image_name').val(imagename);

      var form = $('#form-upload');
      var url = form.attr('action');
      var data = form.serialize();
       

    $.post(url,data).done(function(res){
        window.location.reload(true);
    }).fail(function(res){
         console.log(res)
    });
 return false;

});

fileuploader.on('change',function(){
  // enabled button
  $('#btn_ccw').prop('disabled', false);
  $('#btn_cw').prop('disabled', false);
  $('#btn_submit').prop('disabled', false);
  $('#zooming').prop('disabled', false);

});

// cover photo
var cover_img = $(".cover-img");
var remove = $('#remove');
var reposition = $('#reposition');
var uploading = $('#uploading');
var btn_cancel = $('#btn-cancel');
var btn_upload = $('#btn-upload');


var defaultval = $('#cover_position').val();
cover_img.css('top',defaultval);
cover_img.css( 'pointer-events','none');

cover_img.css('cursor','ns-resize');

var y1 = $('.cover-container').height();
var y2 = $('.cover-img').height();

cover_img.draggable({

        scroll: false,
        axis: "y",                    
        drag: function (event, ui) {
            if (ui.position.top >= 0) {
                ui.position.top = 0;
            }
            else
            if (ui.position.top <= (y1-y2)) {
                ui.position.top = y1-y2;
            }
        },
        stop: function(event, ui) {
        //####
        $('#cover_position').val(ui.position.top);
    }
    });                    

// repositioning
 $('#reposition').on('click',function(){
      cover_img.css( 'pointer-events','');
      remove.addClass('hidden');
      reposition.addClass('hidden');
      uploading.addClass('hidden');
      btn_cancel.removeClass('hidden');
      btn_upload.removeClass('hidden');
 });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('.cover-img')
                .attr('src', e.target.result)      
        };
        $('#remove').addClass('hidden');
        $('#reposition').addClass('hidden');
        $('#uploading').addClass('hidden');
        $('#btn-upload').removeClass('hidden');
        $('#btn-cancel').removeClass('hidden');
        $(".cover-img").css( 'pointer-events','');
        reader.readAsDataURL(input.files[0]);
    }
};
