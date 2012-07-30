# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader
from WhoZwhoCommonFunctions import GetIndexedDirectoryNameLists

def do(request):
    WZ = Z.SetWhoZwho(request, 'Directory')
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ, '')

    name_lists = GetIndexedDirectoryNameLists(WZ)

    if request.COOKIES.has_key('dlist_parm'):
        dlist_parm = request.COOKIES['dlist_parm']
    else:
        dlist_parm = 'F..'

    template = loader.get_template('DirectoryList.html')
    context = Context({
        'browser_tab': WZ['Tabs'][WZ['ActiveTab']][2],
        'first_initials': name_lists[0],
        'first_names': name_lists[1],
        'last_initials': name_lists[2],
        'last_names': name_lists[3],
        'select': dlist_parm.upper(),
        'WZ': WZ,
        })

    return HttpResponse(template.render(context))
