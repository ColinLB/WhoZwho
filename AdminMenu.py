# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

def do(request):
    ZS = Z.SetWhoZwho(request, 'Admin')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    template = loader.get_template('AdminMenu.html')
    context = Context({
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
