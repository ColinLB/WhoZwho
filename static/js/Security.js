/*
Copyright (C) 2012 C. R. Leavett-Brown
You may distribute under the terms of either the GNU General Public
License or the Apache v2 License, as specified in the README file.
*/

function CheckPassword(password, vpassword) {

    /* Character type counter */
    var count = 0;

    /* Loop index */
    var i;              

    /* Search length */
    var search_len;

    /* String of illegal character sequences */
    var Sequences = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 01234567890 qwertyuiop asdfghjkl zxcvbnm zaq1 xsw2 cde3 vfr4 bgt5 nhy6 mju7 ki8 lo9 1qaz 2wsx 3edc 4rfv 5tgb 6yhn 7ujm 8ik 9ol";

    /* Current substring of password to check for character sequences */
    var substr;

    /* Location of substring within illegal sequences */
    var substr_loc;

    if (password.length < 6) return "Error: Password is too short.";

    search_len = password.length-2;
    for (i=0; i<search_len; i++) {
        substr = password.substr(i,3);
        substr_loc = Sequences.search(substr);
        if (substr_loc > -1) return "Error: Password contains recognized character sequences.";
        }

    if (password.match(/[0-9]/)) count++;
    if (password.match(/[a-z]/)) count++;
    if (password.match(/[A-Z]/)) count++;
    if (password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,),`]/)) count++;

    if (count < 3) return "Error: Passwords must use 3 of the 4 character groups: lowercase, uppercase, numeric, and special.";

    if (password != vpassword) return "Error: Passwords do not match.";

    return "";
}

