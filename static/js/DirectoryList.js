/*
Copyright (C) 2012 C. R. Leavett-Brown
You may distribute under the terms of either the GNU General Public
License or the Apache v2 License, as specified in the README file.
*/

function DisplayHideLists(my) {
    var children, firstnode, i;

    if (my == null) {
        firstnode=document.getElementById("F");
        if (firstnode.style.display == 'none') {
            firstnode=document.getElementById("L");
            }
        DisplayHideLists(firstnode);
        }
    else {
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
    var dlist_parm, p1, p2, p3;

    DisplayHideLists();
    document.getElementById(id).style.display = 'block';

    dlist_parm = getCookie("dlist_parm");
    if (dlist_parm === undefined) {
        p2 = '.'; p3 = '.';
        }
    else {
        p2 = dlist_parm.substring(1,2);
        p3 = dlist_parm.substring(2,3);
        }

    p1 = id.substring(0,1);

    if (p1 == "F") {
        p2 = id.substring(1,2);
        }
    else {
        p3 = id.substring(1,2);
        }

    setCookie("dlist_parm", p1 + p2 + p3);
    }

function DisplaySwitchFirstLast() {
    var dlist_parm, first, last, p1, p2;

    dlist_parm = getCookie("dlist_parm");
    if (dlist_parm === undefined) {
        p2 = '..';
        }
    else {
        p2 = dlist_parm.substring(1,3);
        }

    first = document.getElementById('F');
    last = document.getElementById('L');

    if (first.style.display == '' || first.style.display == 'block') {
        first.style.display = 'none';
        last.style.display = 'block';
        p1 = 'L';
        }
    else {
        first.style.display = 'block';
        last.style.display = 'none';
        p1 = 'F';
        }

    setCookie("dlist_parm", p1 + p2);
    }
