$( document ).ready(function() {
    $('#recbutton').click(function(){
        //timeout function with delay else disable click will not work
        setTimeout(function() {
            // disable click almost instantly
            $('#recbutton').prop('disabled', true);
          }, 1); 
          //animation effect
        $('#recbutton').addClass("Rec");  
    });
})