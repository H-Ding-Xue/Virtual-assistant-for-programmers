$("textarea").keydown(function(e){
    // Enter pressed
    if (e.keyCode == 13)
    {
        //method to prevent from default behaviour
        e.preventDefault();
    }
});

ascii = []
for (var i = 33; i < 127; i++)
    ascii.push(String.fromCharCode(i));

asciiNumber = ascii.splice(15,10).join(" ")
asciiUpper = ascii.splice(22,26).join(" ")
asciiLower = ascii.splice(28,26).join(" ")
asciiSymbol = ascii.join(" ")

function inUppercase() {
    var checkBox = document.getElementById("uppercaseI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        if (charIncluded.value == "")
            charIncluded.value += asciiUpper
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiUpper
    }
    else
        charIncluded.value = charIncluded.value.replace(asciiUpper, "").trim()
}

function inLowercase() {
    var checkBox = document.getElementById("lowercaseI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        if (charIncluded.value == "")
            charIncluded.value += asciiLower
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiLower
    }
    else
        charIncluded.value = charIncluded.value.replace(asciiLower, "").trim()
}

function inSymbols() {
    var checkBox = document.getElementById("symbolsI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        if (charIncluded.value == "")
            charIncluded.value += asciiSymbol
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiSymbol
    }
    else
        charIncluded.value = charIncluded.value.replace(asciiSymbol, "").trim()
}

function inNumbers() {
    var checkBox = document.getElementById("numbersI");
    var charIncluded = document.getElementById("charincluded");
    if (checkBox.checked == true) {
        if (charIncluded.value == "")
            charIncluded.value += asciiNumber
        else
            charIncluded.value = charIncluded.value.trim() + " " + asciiNumber
    }
    else
        charIncluded.value = charIncluded.value.replace(asciiNumber, "").trim()
}
  
function exUppercase() {
    var checkBox = document.getElementById("uppercaseE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        if (charExcluded.value == "")
            charExcluded.value += asciiUpper
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiUpper
    }
    else
        charExcluded.value = charExcluded.value.replace(asciiUpper, "").trim()
}

function exLowercase() {
    var checkBox = document.getElementById("lowercaseE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        if (charExcluded.value == "")
            charExcluded.value += asciiLower
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiLower
    }
    else
        charExcluded.value = charExcluded.value.replace(asciiLower, "").trim()
}

function exSymbols() {
    var checkBox = document.getElementById("symbolsE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        if (charExcluded.value == "")
            charExcluded.value += asciiSymbol
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiSymbol
    }
    else
        charExcluded.value = charExcluded.value.replace(asciiSymbol, "").trim()
}

function exNumbers() {
    var checkBox = document.getElementById("numbersE");
    var charExcluded = document.getElementById("charexcluded");
    if (checkBox.checked == true) {
        if (charExcluded.value == "")
            charExcluded.value += asciiNumber
        else
            charExcluded.value = charExcluded.value.trim() + " " + asciiNumber
    }
    else
        charExcluded.value = charExcluded.value.replace(asciiNumber, "").trim()
}