# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from models import Name

def do(request):
    WZ = Z.SetWhoZwho(request, 'Edit')
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    names = Name.objects.all(). \
        exclude(removed__exact=True). \
        filter(owner__exact=WZ['AuthorizedOwner']). \
        order_by('first', 'last')

    template = loader.get_template('DirectoryEditList.html')
    context = Context({
        'browser_tab': WZ['Tabs'][WZ['ActiveTab']][2],
        'names': names,
        'WZ': WZ,
        })

    return HttpResponse(template.render(context))
