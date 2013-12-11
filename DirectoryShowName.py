# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import os.path
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from models import Name
from SessionFunctions import FamilyName, Kids, Birthday

def do(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[SN01]: URL containd an invalid name ID.")

    if not ZS['Approved']:
        if name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[SN02]: URL containd an invalid name ID.")

    template = loader.get_template('DirectoryShowName.html')
    context = Context({
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'name': name,
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
