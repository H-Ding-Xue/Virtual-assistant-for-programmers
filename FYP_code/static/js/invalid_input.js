$(window).keydown(function(e){
    // Enter pressed
    if (e.keyCode == 13)
    {
        //method to prevent from default behaviour
        e.preventDefault();
    }
});

$(document).ready(function() {
    var uppercaseI = document.getElementById("uppercaseI");
    var lowercaseI = document.getElementById("lowercaseI");
    var symbolsI = document.getElementById("symbolsI");
    var numbersI = document.getElementById("numbersI");
    var uppercaseE = document.getElementById("uppercaseE");
    var lowercaseE = document.getElementById("lowercaseE");
    var symbolsE = document.getElementById("symbolsE");
    var numbersE = document.getElementById("numbersE");

    if (uppercaseI.checked == true)
        $("#uppercaseE").attr("disabled", true);
    else
        $("#uppercaseE").removeAttr("disabled");

    if (lowercaseI.checked == true)
        $("#lowercaseE").attr("disabled", true);
    else
        $("#lowercaseE").removeAttr("disabled");
    
    if (symbolsI.checked == true)
        $("#symbolsE").attr("disabled", true);
    else
        $("#symbolsE").removeAttr("disabled");

    if (numbersI.checked == true)
        $("#numbersE").attr("disabled", true);
    else
        $("#numbersE").removeAttr("disabled");
    
    if (uppercaseE.checked == true)
        $("#uppercaseI").attr("disabled", true);
    else
        $("#uppercaseI").removeAttr("disabled");

    if (lowercaseE.checked == true)
        $("#lowercaseI").attr("disabled", true);
    else
        $("#lowercaseI").removeAttr("disabled");
    
    if (symbolsE.checked == true)
        $("#symbolsI").attr("disabled", true);
    else
        $("#symbolsI").removeAttr("disabled");

    if (numbersE.checked == true)
        $("#numbersI").attr("disabled", true);
    else
        $("#numbersI").removeAttr("disabled");
})

ascii = []
for (var i = 33; i < 127; i++)
    ascii.push(String.fromCharCode(i));

asciiNumber = ascii.splice(15,10).join(" ")
asciiUpper = ascii.splice(22,26).join(" ")
asciiLower = ascii.splice(28,26).join(" ")
asciiSymbol = ascii.join(" ")

$("#uppercaseI").click(function(){
    var checkBox = document.getElementById("uppercaseI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        $("#uppercaseE").attr("disabled", true);
        if (charIncluded.value == "")
            charIncluded.value += asciiUpper
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiUpper
    }
    else {
        $("#uppercaseE").removeAttr("disabled");
        charIncluded.value = charIncluded.value.replace(asciiUpper, "").trim()
    }
});

$("#lowercaseI").click(function(){
    var checkBox = document.getElementById("lowercaseI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        $("#lowercaseE").attr("disabled", true);
        if (charIncluded.value == "")
            charIncluded.value += asciiLower
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiLower
    }
    else {
        $("#lowercaseE").removeAttr("disabled");
        charIncluded.value = charIncluded.value.replace(asciiLower, "").trim()
    }
});

$("#symbolsI").click(function(){
    var checkBox = document.getElementById("symbolsI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        $("#symbolsE").attr("disabled", true);
        if (charIncluded.value == "")
            charIncluded.value += asciiSymbol
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiSymbol
    }
    else {
        $("#symbolsE").removeAttr("disabled");
        charIncluded.value = charIncluded.value.replace(asciiSymbol, "").trim()
    }
});

$("#numbersI").click(function(){
    var checkBox = document.getElementById("numbersI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        $("#numbersE").attr("disabled", true);
        if (charIncluded.value == "")
            charIncluded.value += asciiNumber
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiNumber
    }
    else {
        $("#numbersE").removeAttr("disabled");
        charIncluded.value = charIncluded.value.replace(asciiNumber, "").trim()
    }
});
  
$("#uppercaseE").click(function(){
    var checkBox = document.getElementById("uppercaseE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        $("#uppercaseI").attr("disabled", true);
        if (charExcluded.value == "")
            charExcluded.value += asciiUpper
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiUpper
    }
    else {
        $("#uppercaseI").removeAttr("disabled");
        charExcluded.value = charExcluded.value.replace(asciiUpper, "").trim()
    }
});

$("#lowercaseE").click(function(){
    var checkBox = document.getElementById("lowercaseE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        $("#lowercaseI").attr("disabled", true);
        if (charExcluded.value == "")
            charExcluded.value += asciiLower
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiLower
    }
    else {
        $("#lowercaseI").removeAttr("disabled");
        charExcluded.value = charExcluded.value.replace(asciiLower, "").trim()
    }
});

$("#symbolsE").click(function(){
    var checkBox = document.getElementById("symbolsE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        $("#symbolsI").attr("disabled", true);
        if (charExcluded.value == "")
            charExcluded.value += asciiSymbol
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiSymbol
    }
    else {
        $("#symbolsI").removeAttr("disabled");
        charExcluded.value = charExcluded.value.replace(asciiSymbol, "").trim()
    }
});

$("#numbersE").click(function(){
    var checkBox = document.getElementById("numbersE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        $("#numbersI").attr("disabled", true);
        if (charExcluded.value == "")
            charExcluded.value += asciiNumber
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiNumber
    }
    else {
        $("#numbersI").removeAttr("disabled");
        charExcluded.value = charExcluded.value.replace(asciiNumber, "").trim()
    }
});