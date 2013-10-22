# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from models import Name

def do(request):
    ZS = Z.SetSession(request, 'List')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    names = Name.objects.all(). \
        exclude(removed__exact=True). \
        filter(owner__exact=ZS['AuthorizedOwner']). \
        order_by('first', 'last')

    template = loader.get_template('NewROList.html')
    context = Context({
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'names': names,
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
