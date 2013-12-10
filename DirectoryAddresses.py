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
from django.db import models
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader

from models import Address, Family, Name
from SessionFunctions import SaveFileUpload

#
# Create/Edit address form & method.
#
class EditAddressForm(forms.Form):
    street = forms.CharField(max_length=32)
    address_line2 = forms.CharField(max_length=32, required=False)
    municipality = forms.CharField(max_length=32, required=False)
    city = forms.CharField(max_length=32)
    province = forms.CharField(max_length=32)
    country = forms.CharField(max_length=32, required=False)
    postcode = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=32, required=False)
    phone = forms.CharField(max_length=32, required=False)

def EditAddress(request, nid, browser_tab, ZS, option):
    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EA01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[EA02]: URL containd an invalid name ID.")

    address = None
    if option[0] == 'e':
        if option[1] == 'f':
            if name.family:
                if name.family.address:
                    address = name.family.address
        else:
            if name.address:
                address = name.address

        if not address:
            return GoLogout(request, ZS, "[EA01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and address.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[EA05]: URL containd an invalid ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = EditAddressForm(request.POST, request.FILES)
        if form.is_valid():
            if option[0] == 'c':
                address = Address()
                address.owner = name.owner

            address.street = form.cleaned_data['street']
            address.address_line2 = form.cleaned_data['address_line2']
            address.municipality = form.cleaned_data['municipality']
            address.city = form.cleaned_data['city']
            address.province = form.cleaned_data['province']
            address.country = form.cleaned_data['country']
            address.postcode = form.cleaned_data['postcode']
            address.email = form.cleaned_data['email']
            address.phone = form.cleaned_data['phone']
            address.save()

            if option[0] == 'c':
                if option[1] == 'f':
                    name.family.address = address
                else:
                    name.address = address

                name.save()

            logger.info(ZS['User'] + ' EA ' + str(request.POST))

            return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        if option[0] == 'c':
            form = EditAddressForm()
        else:
            form = EditAddressForm(initial={
                'street': address.street,
                'address_line2': address.address_line2,
                'municipality': address.municipality,
                'city': address.city,
                'province': address.province,
                'country': address.country,
                'postcode': address.postcode,
                'email': address.email,
                'phone': address.phone,
                }) 

    context = {
        'browser_tab': browser_tab,
        'form': form,
        'name': name,
        'option': option,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryAddressEdit.html', context )

#
# Address menu method.
#
def Menu(request, nid, browser_tab, ZS, option):
    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EA01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[EA02]: URL containd an invalid name ID.")

    context = {
        'browser_tab': browser_tab,
        'name': name,
        'option': option,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryAddressMenu.html', context )


#
# Create Family Address.
#
def CreateFamily(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    return EditAddress(request, nid, browser_tab, ZS, 'cf')
   
#
# Edit Family Address.
#
def EditFamily(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    return EditAddress(request, nid, browser_tab, ZS, 'ef')
   
#
# Family Address Menu.
#
def FamilyMenu(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    return Menu(request, nid, browser_tab, ZS, 'f')
   
#
# Create Personal Address.
#
def CreatePersonal(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    return EditAddress(request, nid, browser_tab, ZS, 'ci')
   
#
# Edit Personal Address.
#
def EditPersonal(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    return EditAddress(request, nid, browser_tab, ZS, 'ei')
   
#
# Personal Address Menu.
#
def PersonalMenu(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    return Menu(request, nid, browser_tab, ZS, 'i')
   
# Map an Address.
#
def Map(request, aid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    ZS['InitializeBody'] = 1

    try:
        address = Address.objects.get(pk=int(aid))
    except:
        return GoLogout(request, ZS, "[SA01]: URL containd an invalid address ID.")

    if not ZS['Approved']:
        if name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[SA02]: URL containd an invalid address ID.")

    if address.street[0] == '#':
        street = address.street[1:]
    else :
        street = address.street

    if address.municipality:
        map = '+'.join(street.split(' ') + \
            address.municipality.split(' ') + \
            address.province.split(' ') + \
            address.country.split(' '))
    else:
        map = '+'.join(street.split(' ') + \
            address.city.split(' ') + \
            address.province.split(' ') + \
            address.country.split(' '))

    template = loader.get_template('DirectoryAddressMap.html')
    context = Context({
        'address': address,
        'map': map,
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
#
# Shared subfunctions
#
