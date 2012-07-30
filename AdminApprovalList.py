# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

from django.http import HttpResponse
from django.template import Context, loader
from models import Name

def do(request):
    WZ = Z.SetWhoZwho(request, 'Admin')
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ, '')

    names = Name.objects.all(). \
        exclude(removed__exact=True). \
        filter(approved__exact=False). \
        order_by('last', 'first')

    template = loader.get_template('AdminApprovalList.html')
    context = Context({
        'names': names,
        'WZ': WZ,
        })

    return HttpResponse(template.render(context))
