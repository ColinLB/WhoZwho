# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

import os
import time
#import os.path
from subprocess import PIPE, Popen, STDOUT
from datetime import date
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

class DirectoryEditPCForm(forms.Form):
    first = forms.CharField(max_length=32)
    last = forms.CharField(max_length=32)
    cell = forms.CharField(max_length=32, required=False)
    email = forms.EmailField(max_length=32, required=False)
    work_email = forms.EmailField(max_length=32, required=False)
    work_phone = forms.CharField(max_length=32, required=False)
    birthday = DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year - 100, -1)), required=False)
    title = forms.ChoiceField(widget=Select, choices=Z.Titles, required=False)
    gender = forms.ChoiceField(widget=RadioSelect, choices=Z.Genders)

def do(request, nid, browser_tab):
    ZS = Z.SetWhoZwho(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    if nid != '0':
        try:
            name = Name.objects.get(pk=int(nid))
        except:
            return GoLogout(request, ZS, "[PC01]: URL containd an invalid name ID.")

        if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
            return GoLogout(request, ZS, "[PC02]: URL containd an invalid name ID.")

        if ZS['Authority'] >= Z.Admin:
            ZS['AuthorizedOwner'] = name.owner

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditPCForm(request.POST, request.FILES)
        if form.is_valid():
            if nid == '0':
                try:
                    name = Name.objects.get(pk=int(ZS['Nid']))
                except:
                    return GoLogout(request, ZS, "[PC03]: Invalid name ID.")

                new_user = User()
                new_user.username = 'pc' + str(time.time())
                new_user.first_name = form.cleaned_data['first']
                new_user.last_name = form.cleaned_data['last']
                new_user.email = name.user.email
                new_user.save()

                new_name = Name()
                new_name.user = new_user
                new_name.approved = True
                new_name.authority = Z.NewRO
                new_name.private = True
                new_name.owner = name.owner

                new_name.first = form.cleaned_data['first']
                new_name.last = form.cleaned_data['last']
                new_name.email = form.cleaned_data['email']
                new_name.cell = form.cleaned_data['cell']
                new_name.work_email = form.cleaned_data['work_email']
                new_name.work_phone = form.cleaned_data['work_phone']
                new_name.birthday = form.cleaned_data['birthday']
                new_name.title = form.cleaned_data['title']
                new_name.gender = form.cleaned_data['gender']
                new_name.save()
                new_name.save()
            else:
                name.first = form.cleaned_data['first']
                name.last = form.cleaned_data['last']
                name.email = form.cleaned_data['email']
                name.cell = form.cleaned_data['cell']
                name.work_email = form.cleaned_data['work_email']
                name.work_phone = form.cleaned_data['work_phone']
                name.birthday = form.cleaned_data['birthday']
                name.title = form.cleaned_data['title']
                name.gender = form.cleaned_data['gender']
                name.save()

            logger.info(ZS['User'] + ' PC ' + str(request.POST))

            if ZS['ErrorMessage'] == "":
                if ZS['Authority'] >= Z.Admin:
                    return HttpResponseRedirect('/WhoZwho/aelst')
                else:
                    return HttpResponseRedirect('/WhoZwho/delst')
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        if nid == '0':
            form = DirectoryEditPCForm()
            edit_pc_title = 'Add a New Personal Contact'
            addresses = []
            name = None
            schoices = []
            spouse = []
        else:
            form = DirectoryEditPCForm(initial={
                'first': name.first,
                'last': name.last,
                'email': name.email,
                'cell': name.cell,
                'work_email': name.work_email,
                'work_phone': name.work_phone,
                'birthday': name.birthday,
                'title': name.title,
                'gender': name.gender
                }) 

            addresses = Address.objects.all(). \
                filter(owner__exact=ZS['AuthorizedOwner']). \
                order_by('street')

            if name.wedding:
                spouse = name.wedding.name_set.all(). \
                    exclude(id__exact=name.id)
                schoices = []
            else:
                spouse = []
                schoices = Name.objects.all(). \
                    filter(owner__exact=ZS['AuthorizedOwner']). \
                    filter(wedding__exact=None). \
                    exclude(gender__exact=name.gender). \
                    exclude(id__exact=name.id). \
                    order_by('first')

            edit_pc_title = 'Edit Personal Contact: ' + name.first + ' ' + name.last


        context = {
            'EditPCTitle': edit_pc_title,
            'Admin': Z.Admin,
            'addresses': addresses,
            'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
            'form': form,
            'name': name,
            'nid': nid,
            'picture': ZS['httpURL'] + 'static/pics/defaults/greyman.gif',
            'spouse': spouse,
            'schoices': schoices,
            'ZS': ZS
            }

        context.update(csrf(request))
        return render_to_response('DirectoryEditPC.html', context )
