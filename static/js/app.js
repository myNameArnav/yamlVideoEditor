var cm = new CodeMirror.fromTextArea(document.getElementById("CodeMirror"), {
    lineNumbers: true,
    mode: "yaml",
    lineWrapping: true,
    theme: "dracula",
    spellcheck: true,
});

var btnWidth = document.getElementById("btnSubmit").style.width;
var textHeight = (window.innerHeight) * 80 / 100;

cm.setSize(btnWidth, textHeight)