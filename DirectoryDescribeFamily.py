# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

import os.path
from datetime import date
from django.forms.fields import CharField, ChoiceField, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Select, RadioSelect

from django import forms
from django.db import models
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader

from SessionFunctions import ProcessNewPicture
from models import Address, Family, Name


# The Describe Family function has the following subfunctions:
#
#   1. Describe Individual - links a Name object with a Family object.
#   2. Describe a Married Couple Family - object contains two spouses, anniversary, joint email/receipt, and photo,
#      and is a "Parent" target (see #1, above).
#   3. Describe a Single Parent Family - object contains joint email and photo, and is a "Parent" target (see #1, above).
#
# Each subfunction has its own form and method:
#
#
#
# The Individual Request Form & Method:
#
class IndividualChoices(models.Model):
    Select_Address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.DO_NOTHING)
    Select_Parents = models.ForeignKey(Family, blank=True, null=True, on_delete=models.DO_NOTHING)

class DescribeIndividualForm(forms.ModelForm):
    class Meta:
        model = IndividualChoices

def individual(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[DF01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[DF02]: URL containd an invalid name ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = DescribeIndividualForm(request.POST)
        if form.is_valid():
                name.address = form.cleaned_data['Select_Address']
                name.parents = form.cleaned_data['Select_Parents']
                name.save()

                logger.info(ZS['User'] + ' DF ' + str(request.POST))

                return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        selected_address, selected_parents = None, None
        if name.address:
            selected_address = name.address

        if name.parents:
            selected_parents = name.parents

        form = DescribeIndividualForm(initial={
            'Select_Address': selected_address,
            'Select_Parents': selected_parents,
            }) 

    families = Family.objects.all()

    form.fields['Select_Address'].choices = Achoices(name)

    pchoices = [ ['', ''] ]
    for family in families:
        spouses = family.spouses.all()
        if spouses.count() < 2:
            pchoices += [ [family.id, spouses[0].last + ", " + spouses[0].first] ]
        elif spouses[0].gender == 'm':
            pchoices += [ [family.id, spouses[0].last + ", " + spouses[0].first + " & " + spouses[1].first] ]
        else:
            pchoices += [ [family.id, spouses[1].last + ", " + spouses[1].first + " & " + spouses[0].first] ]

    spchoices = sorted(pchoices, key=lambda family_name: family_name[1]) 
    form.fields['Select_Parents'].choices = spchoices

    context = {
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'name': name,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryDescribeIndividual.html', context )

#
# The Married Couple Request Form & Method:
#
class MarriedChoices(models.Model):
    Select_Address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.DO_NOTHING)
    Select_Spouse = models.ForeignKey(Name, blank=True, null=True, on_delete=models.DO_NOTHING)

class DescribeMarriedForm(forms.ModelForm):
    class Meta:
        model = MarriedChoices
    anniversary = DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year - 100, -1)), required=False)
    picture = forms.ImageField(required=False)

def married(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[DF01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[DF02]: URL containd an invalid name ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = DescribeMarriedForm(request.POST)
        if form.is_valid():
            spouse = form.cleaned_data['Select_Spouse']
            if ZS['Authority'] < Z.Admin and spouse.owner != ZS['AuthorizedOwner']:
                ZS['ErrorMessage'] = "[DF03]: Invalid spouse ID selected."

            else: 
                if name.family:
                    family = name.family
                    spouses = family.spouses.all()
                    for remove_spouse in spouses:
                        if remove_spouse.id == name.id or remove_spouse.id == spouse.id:
                            continue
                        remove_spouse.family = None
                        remove_spouse.save()
                else:
                    family = Family()
                    family.owner = name.owner

                family.address = form.cleaned_data['Select_Address']
                family.anniversary = form.cleaned_data['anniversary']
                family.save()

                if request.FILES.has_key('picture'):
                    ZS['ErrorMessage'] = ProcessNewPicture(request, ZS, 'families', str(family.id))

                # Check if the family has a picture and set indicator appropriately.
                if os.path.exists(ZS['StaticPath'] + 'pics/families/' + str(family.id) + '.jpg'):
                    if not family.picture_uploaded:
                        family.picture_uploaded = True
                        family.save()
                else:
                    if family.picture_uploaded:
                        family.picture_uploaded = False
                        family.save()

                name.family = family
                name.save()

                spouse.family = family
                spouse.save()

                logger.info(ZS['User'] + ' DF ' + str(request.POST))

                return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        if name.family:
            selected_address, selected_spouse = None, None
            if name.family.address:
                selected_address = name.family.address

            spouses = name.family.spouses.all(). \
                exclude(id__exact=name.id)

            if spouses:
                selected_spouse = spouses[0]

            form = DescribeMarriedForm(initial={
                'Select_Address': selected_address,
                'Select_Spouse': selected_spouse,
                'anniversary': name.family.anniversary,
                }) 
        else:
            form = DescribeMarriedForm()

    form.fields['Select_Address'].choices = Achoices(name)

    temp_schoices = Name.objects.all(). \
        filter(owner__exact=name.owner). \
        filter(family__exact=None). \
        exclude(gender__exact=name.gender). \
        order_by('first')

    if name.family:
        spouses = name.family.spouses.all(). \
            exclude(id__exact=name.id)
    else:   
        spouses = None

    if spouses:
        schoices = [ ['',''], [spouses[0].id, spouses[0].first + ' ' + spouses[0].last] ]
    else:
        schoices = [ ['',''] ]

    for choice in temp_schoices:
        schoices += [ [choice.id, choice.first + ' ' + choice.last] ]

    form.fields['Select_Spouse'].choices = schoices

    context = {
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'name': name,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryDescribeMarried.html', context )

#
# The Single Parent Family Request Form & Method:
#
class SingleParentChoices(models.Model):
    Select_Address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.DO_NOTHING)

class DescribeSingleParentForm(forms.ModelForm):
    class Meta:
        model = SingleParentChoices
    picture = forms.ImageField(required=False)

def singleparent(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[DF01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[DF02]: URL containd an invalid name ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = DescribeSingleParentForm(request.POST)
        if form.is_valid():
                if name.family:
                    family = name.family
                    spouses = family.spouses.all()
                    for remove_spouse in spouses:
                        if remove_spouse.id != name.id:
                            remove_spouse.family = None
                            remove_spouse.save()
                else:
                    family = Family()
                    family.owner = name.owner

                family.address = form.cleaned_data['Select_Address']
                family.anniversary = None
                family.save()

                if request.FILES.has_key('picture'):
                    ZS['ErrorMessage'] = ProcessNewPicture(request, ZS, 'families', str(family.id))

                # Check if the family has a picture and set indicator appropriately.
                if os.path.exists(ZS['StaticPath'] + 'pics/families/' + str(family.id) + '.jpg'):
                    if not family.picture_uploaded:
                        family.picture_uploaded = True
                        family.save()
                else:
                    if family.picture_uploaded:
                        family.picture_uploaded = False
                        family.save()

                name.family = family
                name.save()

                logger.info(ZS['User'] + ' DF ' + str(request.POST))

                return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        if name.family:
            selected_address = None
            if name.family.address:
                selected_address = name.family.address

            form = DescribeSingleParentForm(initial={
                'Select_Address': selected_address,
                }) 
        else:
            form = DescribeSingleParentForm()

    form.fields['Select_Address'].choices = Achoices(name)

    context = {
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'name': name,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryDescribeSingleParent.html', context )
#
# Achoices: Return a dictionary of address choices.
#
def Achoices(name):
    temp_addresses = Address.objects.all(). \
        filter(owner__exact=name.owner)

    choices = [ ['', ''] ]
    for address in temp_addresses:
#       choice = [ address.street + ', ' + address.city + ', ' + address.province + ', ' + address.postcode ]
        choice = [ address.street ]
        if address.email:
            choice += [ address.email ]

        if address.phone:
            choice += [ address.phone ]

        choices += [ [address.id, ', '.join(choice)] ]

    return sorted(choices, key=lambda address: address[1])
