/*
Borrowed from: http://www.w3schools.com/js/js_cookies.asp
*/

function getCookie(c_name) {
    var i,x,y,ARRcookies=document.cookie.split(";");

    for (i=0;i<ARRcookies.length;i++) {
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name) {
            return unescape(y);
        }
    }
}

function setCookie(c_name, value) {
    var exdays=1;
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    /*
    var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString()) + "; path=/;";
    */
    var c_value=escape(value) + "; path=/;";
    document.cookie=c_name + "=" + c_value;
}
