# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

from models import Address

def do(request, aid, browser_tab):
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ, '')

    WZ['InitializeBody'] = 1

    try:
        address = Address.objects.get(pk=int(aid))
    except:
        return GoLogout(request, WZ, "[SA01]: URL containd an invalid address ID.")

    if not WZ['Approved']:
        if name.owner != WZ['AuthorizedOwner']:
            return GoLogout(request, WZ, "[SA02]: URL containd an invalid address ID.")

    if address.street[0] == '#':
        street = address.street[1:]
    else :
        street = address.street

    if address.municipality:
        map = '+'.join(street.split(' ') + \
            address.municipality.split(' ') + \
            address.province.split(' ') + \
            address.country.split(' '))
    else:
        map = '+'.join(street.split(' ') + \
            address.city.split(' ') + \
            address.province.split(' ') + \
            address.country.split(' '))

    template = loader.get_template('DirectoryShowAddress.html')
    context = Context({
        'address': address,
        'map': map,
        'WZ': WZ,
        })

    return HttpResponse(template.render(context))
