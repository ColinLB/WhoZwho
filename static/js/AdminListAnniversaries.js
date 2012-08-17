/*
Copyright (C) 2012 C. R. Leavett-Brown
You may distribute under the terms of either the GNU General Public
License or the Apache v2 License, as specified in the README file.
*/

function DisplayHideLists(my) {
    var children, firstnode, i;

    if (my == null) {
        firstnode=document.getElementById("X");
        DisplayHideLists(firstnode);
    } else {
        if (my.tagName == "DIV" && my.id.length > 1) {
            my.style.display = 'none';
        }

        children = my.childNodes;
        for (i=0;i<children.length;i++) {
            DisplayHideLists(children[i]);
        }
    }
}

function DisplaySelectedList(id) {
    DisplayHideLists();
    document.getElementById('X1' + id).style.display = 'block';
    document.getElementById('X2' + id).style.display = 'block';
    document.getElementById('X3' + id).style.display = 'block';
}
