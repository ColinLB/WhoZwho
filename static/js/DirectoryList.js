/*
Copyright (C) 2012 C. R. Leavett-Brown
You may distribute under the terms of either the GNU General Public
License or the Apache v2 License, as specified in the README file.
*/

function DirectoryListABC(opt) {
    var dlist_parm, p1, p2, p3;

    p1 = opt.substring(0,1);

    SelectHTMLdiv('i' + p1, 'i' + opt, 'text_selected', 'text_deselected');
    SelectHTMLdiv('l' + p1, 'l' + opt);

    dlist_parm = getCookie("dlist_parm");
    if (dlist_parm === undefined) {
        p2 = '.'; p3 = '.';
        }
    else {
        p2 = dlist_parm.substring(1,2);
        p3 = dlist_parm.substring(2,3);
        }

    if (p1 == "F") {
        p2 = opt.substring(1,2);
        }
    else {
        p3 = opt.substring(1,2);
        }

    setCookie("dlist_parm", p1 + p2 + p3);
    }

function DirectoryListFLMW(opt) {
    var dlist_parm, p2;

    SelectHTMLdiv('subtabs', 'subtabs' + opt, 'subtabs_selected', 'subtabs_deselected');
    SelectHTMLdiv('List', 'List' + opt);

    dlist_parm = getCookie("dlist_parm");
    if (dlist_parm === undefined) {
        p2 = '..';
    } else {
        p2 = dlist_parm.substring(1,3);
    }

    setCookie("dlist_parm", opt + p2);
}
