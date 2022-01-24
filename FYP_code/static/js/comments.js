$( document ).ready(function() {
    // use tab as indentation instead of going to next element
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