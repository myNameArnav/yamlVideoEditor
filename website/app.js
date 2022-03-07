var cm = new CodeMirror.fromTextArea(document.getElementById("CodeMirror"), {
    lineNumbers: true,
    mode: "yaml",
    lineWrapping: true,
    theme: "dracula",
    spellcheck: true
});
cm.setSize()
    // console.log("hello")

// console.log(document.getElementById("CodeMirror").value)

// config = document.getElementById("CodeMirror").value

function download_txt() {
    var textToSave = document.getElementById("CodeMirror").value;
    var hiddenElement = document.createElement('a');

    hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'myFile.yaml';
    hiddenElement.click();
}

document.getElementById("btnSubmit").addEventListener('click', download_txt);