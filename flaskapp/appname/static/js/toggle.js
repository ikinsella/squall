function toggleButton(buttonId, textId, text) {
    if (document.getElementById(textId).innerHTML == "") {
        document.getElementById(textId).innerHTML = text;
        document.getElementById(buttonId).innerHTML = "hide";
    } else {
        document.getElementById(textId).innerHTML = "";
        document.getElementById(buttonId).innerHTML = "info";
    }

}