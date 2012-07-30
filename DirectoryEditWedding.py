# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
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

from models import Name, Wedding

class DirectoryChooseSuitorModel(models.Model):
    Select_Spouse = models.ForeignKey(Name)

class DirectoryEditWeddingForm(forms.ModelForm):
    class Meta:
        model = DirectoryChooseSuitorModel
    anniversary = DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year - 100, -1)), required=False)
    Joint_Email = forms.EmailField(max_length=32, required=False)

def do(request, nid, browser_tab):
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, WZ, "[EW01]: URL containd an invalid name ID.")

        if WZ['Authority'] < Z.Admin and name.owner != WZ['AuthorizedOwner']:
            return GoLogout(request, WZ, "[EW02]: URL containd an invalid name ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditWeddingForm(request.POST)
        if form.is_valid():
            spouse = form.cleaned_data['Select_Spouse']
            if WZ['Authority'] < Z.Admin and spouse.owner != WZ['AuthorizedOwner']:
                WZ['ErrorMessage'] = "[EW03]: Invalid spouse ID selected."

            else: 
                if name.wedding:
                    wedding = name.wedding
                    family = wedding.name_set.all()
                    for member in family:
                        if member.id == name.id or member.id == spouse.id:
                            continue
                        member.wedding = None
                        member.save()
                else:
                    wedding = Wedding()
                    wedding.owner = name.owner

                wedding.anniversary = form.cleaned_data['anniversary']
                wedding.email = form.cleaned_data['Joint_Email']
                wedding.save()

                name.wedding_id = wedding.id
                name.save()

                spouse.wedding_id = wedding.id
                spouse.save()

                logger.info(WZ['User'] + ' EW ' + str(request.POST))

                return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        if name.wedding:
            form = DirectoryEditWeddingForm(initial={
                'anniversary': name.wedding.anniversary,
                'Joint_Email': name.wedding.email,
                }) 
        else:
            form = DirectoryEditWeddingForm()

    temp_schoices = Name.objects.all(). \
        filter(owner__exact=name.owner). \
        filter(wedding__exact=None). \
        exclude(gender__exact=name.gender). \
        exclude(id__exact=name.id). \
        order_by('first')

    if name.wedding:
        spouse = name.wedding.name_set.all(). \
            exclude(id__exact=name.id)

        schoices = [ [spouse[0].id, spouse[0].first + ' ' + spouse[0].last] ]
    else:
        schoices = [ ]

    for choice in temp_schoices:
        schoices += [ [choice.id, choice.first + ' ' + choice.last] ]

    form.fields['Select_Spouse'].choices = schoices

    if name.wedding:
        EditWeddingTitle = 'Edit Wedding: ' + name.first + ' & ' + spouse[0].first + ' ' + name.last
    else:
        EditWeddingTitle = 'Add Wedding: ' + name.first + ' ' + name.last

    context = {
        'EditWeddingTitle': EditWeddingTitle,
        'browser_tab': WZ['Tabs'][WZ['ActiveTab']][2],
        'form': form,
        'nid': nid,
        'WZ': WZ
        }

    context.update(csrf(request))
    return render_to_response('DirectoryEditWedding.html', context )

def dont(request, nid, browser_tab):
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, WZ, "[EW04]: URL containd an invalid name ID.")

        if WZ['Authority'] < Z.Admin and name.owner != WZ['AuthorizedOwner']:
            return GoLogout(request, WZ, "[EW05]: URL containd an invalid name ID.")

    wedding = name.wedding

    family = wedding.name_set.all()

    for member in family:
        member.wedding = None
        member.save()

    wedding.delete()

    logger.info(WZ['User'] + ' EW ' + str(request.POST))

    return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
