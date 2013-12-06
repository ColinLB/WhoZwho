# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

from django.forms.fields import ChoiceField
from django.forms.widgets import Select

from django import forms
from django.db import models
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader

from models import Address, Name

class DirectoryChooseAddressModel(models.Model):
    Choose_Address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.DO_NOTHING)

class DirectoryChooseAddressForm(forms.ModelForm):
    class Meta:
        model = DirectoryChooseAddressModel

def do(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[CA01]: URL contained an invalid name ID.")

    if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
        return GoLogout(request, ZS, "[CA02]: URL contained an invalid name ID.")

    if ZS['Authority'] >= Z.Admin:
        ZS['AuthorizedOwner'] = name.owner

    addresses = Address.objects.all(). \
        filter(owner__exact=ZS['AuthorizedOwner']). \
        order_by('street')

    achoices = []
    for address in addresses:
        achoices += [ [ address.id, address.street + ', ' + address.city + ', ' + address.province + ', ' + address.postcode ] ]

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryChooseAddressForm(request.POST)
        if form.is_valid():
            try:
                address = Address.objects.get(pk=int(form.cleaned_data['Choose_Address'].id))
            except:
                return GoLogout(request, ZS, "[CA03]: Choice contained an invalid address ID.")

            if address.owner != ZS['AuthorizedOwner']:
                return GoLogout(request, ZS, "[CA04]: Choice contained an invalid address ID.")

            name.address_id = address.id
            name.save()

            logger.info(ZS['User'] + ' CA ' + str(request.POST))

            return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)

    if not name.address:
        form = DirectoryChooseAddressForm()
    else:
        form = DirectoryChooseAddressForm(initial = {
            'Choose_Address': name.address.id,
            })

    form.fields['Choose_Address'].choices = achoices

    context = {
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'name': name,
        'nid': nid,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryChooseAddress.html', context )
