$(document).ready(function() {
    $("[href]").each(function() {
        if (this.href == window.location.href) {
            $(this).addClass("active");
        }
    });

    // set alerts to display for only 3s if any
    setInterval(function(){ $(".alert").fadeOut(); }, 3000);

    $('#voicebot').click(function(){
        //timeout function with delay else disable click will not work
        setTimeout(function() {
            // disable click almost instantly
            $('#voicebot').prop('disabled', true);
            }, 1); 
            //animation effect
        $('#voicebot').removeClass("btn btn-secondary").addClass("btn btn-danger");  
        $('#spantext').html("<b>Recording voice...");

    });
});