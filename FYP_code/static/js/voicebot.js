$( document ).ready(function() {    
    $('#recButton').click(function(){
        //timeout function with delay else disable click will not work
        setTimeout(function() {
            // disable click almost instantly
            $('#recButton').prop('disabled', true);
          }, 1); 
          //animation effect
        $('#recButton').addClass("Rec");  
        $('#rectext').html("<b>Recording in process.... </b><br/>Recording will automatically stop when no voice is detected.");

    });
})