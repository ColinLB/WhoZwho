/*
Copyright (C) 2012 C. R. Leavett-Brown
You may distribute under the terms of either the GNU General Public
License or the Apache v2 License, as specified in the README file.
*/

function SelectHTMLdiv(root, tree, select_class, deselect_class, self) {
    var children, firstnode, i, x;

    if (self == null) {
        firstnode=document.getElementById(root);
        SelectHTMLdiv(root, tree, select_class, deselect_class, firstnode);
    } else {
        if (self.id.length > root.length && self.id.substring(0, root.length) == root) {
            x=self.id.substring(0, root.length)
            if (self.id == tree) {
                if (select_class == null) {
                    self.style.display = 'block';
                } else {
                    self.className = select_class;
                }
            } else {
                if (select_class == null) {
                    self.style.display = 'none';
                } else {
                    self.className = deselect_class;
                }
            }
        }

        children = self.childNodes;
        for (i=0;i<children.length;i++) {
            if (children[i].tagName == 'DIV' || children[i].tagName == 'A') {
                SelectHTMLdiv(root, tree, select_class, deselect_class, children[i]);
            }
        }
    }
}
