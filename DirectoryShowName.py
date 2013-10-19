# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import os.path
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from models import Name

def do(request, nid, browser_tab):
    ZS = Z.SetWhoZwho(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[SN01]: URL containd an invalid name ID.")

    if not ZS['Approved']:
        if name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[SN02]: URL containd an invalid name ID.")

    try:
        birthday = Z.Months[name.birthday.month - 1] + ', ' + str(name.birthday.day)
    except:
        birthday = ""

    try:
        gender = Z.Genders[name.gender]
    except:
        gender = ""

    try:
        title = Z.Titles[name.title]
    except:
        title = ""

    if os.path.exists(ZS['StaticPath'] + 'pics/names/' + str(name.id) + '.jpg'):
        picture = ZS['httpURL'] + 'static/pics/names/' + str(name.id) + '.jpg'
    else:
        if name.private == False:
            picture = ZS['httpURL'] + 'static/pics/defaults/greenman.gif'
        else:
            picture = ZS['httpURL'] + 'static/pics/defaults/greyman.gif'

    if name.wedding:
        spouse = name.wedding.name_set.all(). \
            exclude(id__exact=name.id)

        if os.path.exists(ZS['StaticPath'] + 'pics/names/' + str(spouse[0].id) + '.jpg'):
            spicture = ZS['httpURL'] + 'static/pics/names/' + str(spouse[0].id) + '.jpg'
        else:
            if name.private == False:
                spicture = ZS['httpURL'] + 'static/pics/defaults/greenman.gif'
            else:
                spicture = ZS['httpURL'] + 'static/pics/defaults/greyman.gif'
    else:
        spicture = ''
        spouse = []

    template = loader.get_template('DirectoryShowName.html')
    context = Context({
        'name': name,
        'birthday': birthday,
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'gender': gender,
        'title': title,
        'picture': picture,
        'spicture': spicture,
        'spouse': spouse,
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
