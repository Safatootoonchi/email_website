function myFunction0(style) {
    var sel = window.getSelection();
    if (sel.rangeCount) {

        var e = document.createElement('span');
        e.classList.add("none");
        e.innerHTML = sel.toString();

        var range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(e);
    }
}




function myFunction1(style) {
    var sel = window.getSelection();
    if (sel.rangeCount) {

        var e = document.createElement('span');
        e.classList.add("bolded");
        e.innerHTML = sel.toString();

        range.deleteContents();
        range.insertNode(e);
    }
}




function myFunction2(style) {
    var sel = window.getSelection();
    if (sel.rangeCount) {

        var e = document.createElement('span');
        e.classList.add("underline");
        e.innerHTML = sel.toString();

        var range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(e);
    }
}




function myFunction3(style) {
    var sel = window.getSelection();
    if (sel.rangeCount) {

        var e = document.createElement('span');
        e.classList.add("italic");
        e.innerHTML = sel.toString();

        var range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(e);
    }
}


function Bold() {
    document.getElementById("text").style.fontWeight = 'bold';

}

function Italic() {
    document.getElementById("text").style.fontStyle = 'italic';

}

function red(style) {
    var sel = window.getSelection();
    if (sel.rangeCount) {

        var e = document.createElement('span');
        e.classList.add("red");
        e.innerHTML = sel.toString();

        var range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(e);
    }
}

function green(style) {
    var sel = window.getSelection();
    if (sel.rangeCount) {

        var e = document.createElement('span');
        e.classList.add("green");
        e.innerHTML = sel.toString();

        var range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(e);
    }
}
function blue(style) {
    var sel = window.getSelection();
    if (sel.rangeCount) {

        var e = document.createElement('span');
        e.classList.add("blue");
        e.innerHTML = sel.toString();

        var range = sel.getRangeAt(0);
        range.deleteContents();
        range.insertNode(e);
    }
}
