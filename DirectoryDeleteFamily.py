# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

from django.http import HttpResponseRedirect
from models import Family, Name

def nofamily(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[DF04]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[DF05]: URL containd an invalid name ID.")

    if name.family:
        family = name.family

        spouses = family.spouses.all()
        for spouse in spouses:
            spouse.family = None
            spouse.save()

        children = family.children.all()
        for child in children:
            child.parents = None
            child.save()

        family.delete()

    logger.info(ZS['User'] + ' DF ' + str(request.POST))

    return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
