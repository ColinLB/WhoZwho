# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader
from SessionFunctions import GetIndexedDirectoryNameLists

def do(request):
    ZS = Z.SetSession(request, 'Directory')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    name_lists = GetIndexedDirectoryNameLists(ZS)

    if request.COOKIES.has_key('dlist_parm'):
        dlist_parm = request.COOKIES['dlist_parm']
    else:
        dlist_parm = 'F..'

    template = loader.get_template('DirectoryList.html')
    context = Context({
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'first_initials': name_lists[0],
        'first_names': name_lists[1],
        'last_initials': name_lists[2],
        'last_names': name_lists[3],
        'select': dlist_parm.upper(),
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
