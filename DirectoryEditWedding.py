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

from models import Name, Wedding

class DirectoryChooseSuitorModel(models.Model):
    Select_Spouse = models.ForeignKey(Name)

class DirectoryEditWeddingForm(forms.ModelForm):
    class Meta:
        model = DirectoryChooseSuitorModel
    anniversary = DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year - 100, -1)), required=False)
    Joint_Email = forms.EmailField(max_length=32, required=False)

def do(request, nid, browser_tab):
    ZS = Z.SetWhoZwho(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EW01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[EW02]: URL containd an invalid name ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditWeddingForm(request.POST)
        if form.is_valid():
            spouse = form.cleaned_data['Select_Spouse']
            if ZS['Authority'] < Z.Admin and spouse.owner != ZS['AuthorizedOwner']:
                ZS['ErrorMessage'] = "[EW03]: Invalid spouse ID selected."

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

                logger.info(ZS['User'] + ' EW ' + str(request.POST))

                if name.private == True:
                    return HttpResponseRedirect('/WhoZwho/editpc/' + nid + '/' + browser_tab)
                else:
                    return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
        else:
            ZS['ErrorMessage'] = str(form.errors)
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
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'nid': nid,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryEditWedding.html', context )

def dont(request, nid, browser_tab):
    ZS = Z.SetWhoZwho(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EW04]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[EW05]: URL containd an invalid name ID.")

    wedding = name.wedding

    family = wedding.name_set.all()

    for member in family:
        member.wedding = None
        member.save()

    wedding.delete()

    logger.info(ZS['User'] + ' EW ' + str(request.POST))

    if name.private == True:
        return HttpResponseRedirect('/WhoZwho/editpc/' + nid + '/' + browser_tab)
    else:
        return HttpResponseRedirect('/WhoZwho/ename/' + nid + '/' + browser_tab)
