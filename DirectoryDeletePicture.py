# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

from os import system
from time import time
from datetime import date
from subprocess import PIPE, Popen, STDOUT
from django.forms.fields import ChoiceField, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Select, RadioSelect

from django import forms
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.contrib.auth.models import User

from models import Address, Name, Wedding
from WhoZwhoCommonFunctions import SaveFileUpload

def do(request, nid, browser_tab):
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, WZ, "[EN01]: URL contained an invalid name ID.")

    if WZ['Authority'] < Z.Admin and name.owner != WZ['AuthorizedOwner']:
        return GoLogout(request, WZ, "[EN02]: URL contained an invalid name ID.")

    p = Popen(['/bin/mv',
        WZ['StaticPath'] + 'pics/names/' + nid +'.jpg',
        WZ['StaticPath'] + 'pics/names/old/' + nid + '.jpg' + '.' + str(int(time()))],
        stdout=PIPE, stderr=PIPE)

    stdout, stderr = p.communicate()
    if stderr != '':
        return  "[EN03]: /bin/mv error - " + stderr

    if WZ['Authority'] >= Z.Admin:
        return HttpResponseRedirect('/WhoZwho/aelst')
    else:
        return HttpResponseRedirect('/WhoZwho/delst')
