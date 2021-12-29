$( document ).ready(function() {
    // set alerts to display for only 3s if any
    setInterval(function(){ $(".alert").fadeOut(); }, 3000);
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