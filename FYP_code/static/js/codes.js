$( document ).ready(function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(function(stream) {
            // if microphone access is given
            $('#recbutton').addClass("notRec");
            $('#recbutton').click(function(){
                event.preventDefault();
                if($('#recbutton').hasClass('notRec')){
                    $('#recbutton').removeClass("notRec");
                    $('#recbutton').addClass("Rec");
                    $('#icn').removeClass("fas fa-microphone-alt fa-3x");
                    $('#icn').addClass("fas fa-stop fa-3x");
                }
                else{
                    $('#recbutton').removeClass("Rec");
                    $('#icn').removeClass("fas fa-stop fa-3x");
                    $('#icn').addClass("fas fa-microphone-alt fa-3x");
                    $('#recbutton').addClass("notRec");
                }
            });
      })
      .catch(function(err) {
        // if microphone access is blocked
        alert('Please allow microphone access in order to use voice assistant.')
      });
})