/*
Copyright (C) 2012 C. R. Leavett-Brown
You may distribute under the terms of either the GNU General Public
License or the Apache v2 License, as specified in the README file.
*/

function DirectoryListSwitchRe() {
    var re, tab, tabre;

    tabre = DirectoryListSaveParms();
    tab = tabre.substring(0,1);
    re = tabre.substring(1);

    if (re != '^' & re != ',') {
        DirectoryListSelect(tab, re);
    }
}

function DirectoryListSwitchTab(tabID) {
    var re, tab, tabre;

    tabre = DirectoryListSaveParms(tabID);
    tab = tabre.substring(0,1);
    re = tabre.substring(1);

    SelectHTMLdiv('subtabs', 'subtabs' + tab, 'subtabs_selected', 'subtabs_deselected');
    SelectHTMLdiv('List', 'List' + tab);
    DirectoryListSelect(tab, re);
}

function DirectoryListSaveParms(tabID) { 
    var parm, re, tab;

    if (tabID == null) {
        parm = getCookie("dlist_parm");
        if (parm != null) {
            tab = parm.substring(0,1).toUpperCase();
        } else {
            tab = 'C';
        }
    } else {
        tab = tabID.substring(0,1).toUpperCase();
    }

    re = document.getElementById('selector').value.toLowerCase();
    setCookie("dlist_parm", tab + re);
    return tab + re
}

function DirectoryListSelect(tab, re, self) { 
    var children, i, root;

    root = 'List' + tab

    if (self == null) { 
        if (re == '') {
            DirectoryListSelect(tab, re, document.getElementById(root));
        } else {
            DirectoryListSelect(tab, new RegExp(re), document.getElementById(root));
        }

    } else {
        if (self.id == root || re == '' || self.id.toLowerCase().search(re) != -1) { 
            self.style.display = 'block';
        } else {
            self.style.display = 'none'; 
        }       

        children = self.childNodes;
        for (i=0;i<children.length;i++) {
            if (children[i].tagName == 'DIV') {
                DirectoryListSelect(tab, re, children[i]);
            }       
        }       
    }       
}
