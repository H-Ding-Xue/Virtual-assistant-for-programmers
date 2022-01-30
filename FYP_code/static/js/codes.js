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
    $("textarea").keydown(function(e) {
        if(e.keyCode === 9) { 
            var start = this.selectionStart;
            var end = this.selectionEnd;
    
            var $this = $(this);
    
            $this.val($this.val().substring(0, start)
                        + "    "  
                        + $this.val().substring(end));
    
            this.selectionStart = this.selectionEnd = start + 4;
    
            return false;
        }
    });
})