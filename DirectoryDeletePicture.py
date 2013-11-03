# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import os
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
from SessionFunctions import SaveFileUpload

def do(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EN01]: URL contained an invalid name ID.")

    if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
        return GoLogout(request, ZS, "[EN02]: URL contained an invalid name ID.")

    os.environ['PATH'] = ZS['PythonPath']
    p = Popen(['rm', '-f',
        ZS['StaticPath'] + 'pics/names/' + nid +'.jpg'],
        stdout=PIPE, stderr=PIPE)

    stdout, stderr = p.communicate()
    if stderr != '':
        return  "[EN03]: command error (rm) - " + stderr

    name.picture_uploaded = False
    name.save()

    if ZS['Authority'] >= Z.Admin:
        return HttpResponseRedirect('/WhoZwho/aelst')
    else:
        return HttpResponseRedirect('/WhoZwho/delst')
