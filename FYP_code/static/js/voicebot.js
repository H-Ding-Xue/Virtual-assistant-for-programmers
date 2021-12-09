$( document ).ready(function() {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(function(stream) {
            // if microphone access is given
            $('#recButton').addClass("notRec");
            $('#recButton').click(function(){
                if($('#recButton').hasClass('notRec')){
                    $('#recButton').removeClass("notRec");
                    $('#recButton').addClass("Rec");
                    $('#icon').removeClass("fas fa-microphone-alt fa-5x");
                    $('#icon').addClass("fas fa-stop fa-5x");
                    $('#rectext').html("<b>Recording in process.... </b><br/>Click on the button again when you are done speaking.");
                    
                }
                else{
                    $('#recButton').removeClass("Rec");
                    $('#icon').removeClass("fas fa-stop fa-5x");
                    $('#icon').addClass("fas fa-microphone-alt fa-5x");
                    $('#recButton').addClass("notRec");
                    $('#rectext').html("Recording done. Click on the button above to start the voice assistant again.");
                }
            });
      })
      .catch(function(err) {
        // if microphone access is blocked
        alert('Please allow microphone access in order to use voice assistant.')
      });
})