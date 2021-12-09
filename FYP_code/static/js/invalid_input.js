$( document ).ready(function() {
    $("form").submit(function(){
       event.preventDefault();
       $('#output').prop("disabled", false); // enable text area
});
})