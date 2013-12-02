# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
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

from models import Address, Family, Name
from SessionFunctions import SaveFileUpload

def do(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    # Retrieve name to purge and ensure we have the authority.
    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[BN01]: URL contained an invalid name ID.")

    if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
        return GoLogout(request, ZS, "[BN02]: URL contained an invalid name ID.")

    os.environ['PATH'] = ZS['PythonPath']

    # Free the address.
    if name.address:
        name.address = None
        name.save()

        # Purge ALL unused addresses.
        addresses = Address.objects.all()
        for address in addresses:
            if address.name_set.count() < 1:
                logger.info(ZS['User'] + ' BN Unused address deleted: id=' + str(address.id) + ', ' + \
                    address.street + ', ' + address.city + ', ' + address.province + ', ' + address.postcode)
                address.delete()


    # If there is connected family, save family pointer and disconnect it.
    if name.family:
        family = name.family
        name.family = None
        name.save()

        # If the disconnected family has no remaining spouses, disconnect all children ...
        if family.spouses.count() < 1:
            children = family.children.all()
            for child in children:
                child.parents = None
                child.save()

            # ... remove the family picture ...
            p = Popen(['rm', '-f',
                ZS['StaticPath'] + 'pics/families/' + str(family.id) +'.jpg'],
                stdout=PIPE, stderr=PIPE)

            stdout, stderr = p.communicate()
            if stderr != '':
                logger.info(ZS['User'] + ' BN Command error deleting family picture: id=' + str(family.id) + ', ' + \
                    stderr)

            # ... and purge the family.
            logger.info(ZS['User'] + ' BN Unused family deleted: id=' + str(family.id) + ', ' + \
                name.last + ', ' + name.first)
            family.delete()

    # Remove the personal picture.
    p = Popen(['rm', '-f',
        ZS['StaticPath'] + 'pics/names/' + str(name.id) +'.jpg'],
        stdout=PIPE, stderr=PIPE)

    stdout, stderr = p.communicate()
    if stderr != '':
        logger.info(ZS['User'] + ' BN Command error deleting personal picture: id=' + str(name.id) + ', ' + \
            stderr)

    # Purge the person.
    logger.info(ZS['User'] + ' BN Name deleted: id=' + str(name.id) + ', ' + \
        name.first + ' ' + name.last)
    name.user.delete()
    name.delete()

    if ZS['Authority'] >= Z.Admin:
        return HttpResponseRedirect('/WhoZwho/aelst')
    else:
        return HttpResponseRedirect('/WhoZwho/delst')
