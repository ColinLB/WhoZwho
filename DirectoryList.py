# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout
from urllib import unquote

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader
from SessionFunctions import GetDirectoryLists

def do(request):
    ZS = Z.SetSession(request, 'Directory')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    ZS['InitializeBody'] = 1

    name_lists = GetDirectoryLists(ZS)

    if request.COOKIES.has_key('dlist_parm'):
        dlist_parm = unquote(request.COOKIES['dlist_parm'])
    else:
        dlist_parm = 'C'

    template = loader.get_template('DirectoryList.html')
    context = Context({
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'church_list': name_lists[0],
        'friend_list': name_lists[1],
        'select_tab': dlist_parm[0].upper(),
        'select_re': dlist_parm[1:],
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
