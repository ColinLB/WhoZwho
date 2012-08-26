# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

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
from WhoZwhoCommonFunctions import SaveFileUpload

def do(request, nid, browser_tab):
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, WZ, "[BN01]: URL contained an invalid name ID.")

    if WZ['Authority'] < Z.Admin and name.owner != WZ['AuthorizedOwner']:
        return GoLogout(request, WZ, "[BN02]: URL contained an invalid name ID.")

    os.environ['PATH'] = WZ['PythonPath']
    p = Popen(['rm', '-f',
        WZ['StaticPath'] + 'pics/names/' + nid +'.jpg'],
        stdout=PIPE, stderr=PIPE)

    stdout, stderr = p.communicate()
    if stderr != '':
        return  "[BN03]: command error (rm) - " + stderr

    owner = name.owner
    logger.info(WZ['User'] + ' BN User and Name deleted for ID ' + str(nid) + ', ' + name.first + ' ' + name.last + '.')
    User.objects.filter(id=name.user.id).delete()
    Name.objects.filter(id=name.id).delete()

    addresses = Address.objects.all(). \
        filter(owner__exact=owner). \
        order_by('street')

    for address in addresses:
        names = address.name_set.all()
        if len(names) < 1:
            logger.info(WZ['User'] + ' BN Unused address deleted for owner ' + \
                str(owner) + ': ' + address.street + ', ' + address.city + ', ' + \
                address.province + ', ' + address.postcode)
            address.delete()

    weddings = Wedding.objects.all(). \
        filter(owner__exact=owner)

    for wedding in weddings:
        names = wedding.name_set.all()
        if len(names) < 1:
            logger.info(WZ['User'] + ' BN Unused wedding deleted for owner ' + \
                str(owner) + ': ' + str(wedding.anniversary) + '.')
            wedding.delete()

    if WZ['Authority'] >= Z.Admin:
        return HttpResponseRedirect('/WhoZwho/aelst')
    else:
        return HttpResponseRedirect('/WhoZwho/delst')
