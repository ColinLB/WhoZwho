# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

import os.path
from django.forms.fields import ChoiceField, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Select, RadioSelect

from django import forms
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader

from models import Address, Name
from SessionFunctions import SaveFileUpload

class DirectoryEditAddressForm(forms.Form):
    street = forms.CharField(max_length=32)
    address_line2 = forms.CharField(max_length=32, required=False)
    municipality = forms.CharField(max_length=32, required=False)
    city = forms.CharField(max_length=32)
    province = forms.CharField(max_length=32)
    country = forms.CharField(max_length=32, required=False)
    postcode = forms.CharField(max_length=32)
    home_phone = forms.CharField(max_length=32, required=False)

def do(request, nid, aid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EA01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[EA02]: URL containd an invalid name ID.")

    if aid != '0':
        try:
            address = Address.objects.get(pk=int(aid))
        except:
            return GoLogout(request, ZS, "[EA03]: URL containd an invalid addressID.")

        if address.owner != name.owner:
            return GoLogout(request, ZS, "[EA04]: URL containd an invalid address ID.")

        if ZS['Authority'] < Z.Admin and address.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[EA05]: URL containd an invalid ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditAddressForm(request.POST, request.FILES)
        if form.is_valid():
            if aid == '0':
                address = Address()
                address.owner = name.owner

            address.street = form.cleaned_data['street']
            address.address_line2 = form.cleaned_data['address_line2']
            address.municipality = form.cleaned_data['municipality']
            address.city = form.cleaned_data['city']
            address.province = form.cleaned_data['province']
            address.country = form.cleaned_data['country']
            address.postcode = form.cleaned_data['postcode']
            address.phone = form.cleaned_data['home_phone']
            address.save()

            if aid == '0':
                name.address_id = address.id
                name.save()

            logger.info(ZS['User'] + ' EA ' + str(request.POST))

            return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        if aid == '0':
            form = DirectoryEditAddressForm()
        else:
            form = DirectoryEditAddressForm(initial={
                'street': address.street,
                'address_line2': address.address_line2,
                'municipality': address.municipality,
                'city': address.city,
                'province': address.province,
                'country': address.country,
                'postcode': address.postcode,
                'home_phone': address.phone,
                }) 

    if aid == '0':
        EditAddressTitle = 'Add New Address:'
    else:
        EditAddressTitle = 'Edit Address: ' + address.street

    context = {
        'EditAddressTitle': EditAddressTitle,
        'aid': aid,
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'nid': nid,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryEditAddress.html', context )
