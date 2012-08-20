# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
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
from WhoZwhoCommonFunctions import SaveFileUpload

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
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, WZ, "[EN01]: URL contained an invalid name ID.")

    if WZ['Authority'] < Z.Admin and name.owner != WZ['AuthorizedOwner']:
        return GoLogout(request, WZ, "[EN02]: URL contained an invalid name ID.")

    if WZ['Authority'] >= Z.Admin:
        WZ['AuthorizedOwner'] = name.owner

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditPCForm(request.POST, request.FILES)
        if form.is_valid():
            users = User.objects.all().filter(username__exact=form.cleaned_data['Login_ID']).exclude(id__exact=name.user.id)
            if len(users) < 1:
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

                if name.user.username != form.cleaned_data['Login_ID'] or name.user.email != form.cleaned_data['Account_Email']:
                    name.user.username = form.cleaned_data['Login_ID']
                    name.user.email = form.cleaned_data['Account_Email']
                    name.user.save()

                logger.info(WZ['User'] + ' EN ' + str(request.POST))

                if request.FILES.has_key('picture'):
                    WZ['ErrorMessage'] = ProcessNewPicture(request, WZ, nid)

                if WZ['ErrorMessage'] == "":
                    if WZ['Authority'] >= Z.Admin:
                        return HttpResponseRedirect('/WhoZwho/aelst')
                    else:
                        return HttpResponseRedirect('/WhoZwho/delst')
            else:
                WZ['ErrorMessage'] = "[EN03]: Login ID already used, choose another."
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        form = DirectoryEditPCForm(initial={
            'Login_ID': name.user.username,
            'first': name.first,
            'last': name.last,
            'email': name.email,
            'cell': name.cell,
            'work_email': name.work_email,
            'work_phone': name.work_phone,
            'Account_Email': name.user.email,
            'birthday': name.birthday,
            'title': name.title,
            'gender': name.gender
            }) 

    if os.path.exists(WZ['StaticPath'] + 'pics/names/' + str(name.id) + '.jpg'):
        picture = WZ['httpURL'] + 'static/pics/names/' + str(name.id) + '.jpg'
    else:
        picture = WZ['httpURL'] + 'static/pics/names/default.jpg'

    addresses = Address.objects.all(). \
        filter(owner__exact=WZ['AuthorizedOwner']). \
        order_by('street')

    if name.wedding:
        spouse = name.wedding.name_set.all(). \
            exclude(id__exact=name.id)
        schoices = []
    else:
        spouse = []
        schoices = Name.objects.all(). \
            filter(owner__exact=WZ['AuthorizedOwner']). \
            filter(wedding__exact=None). \
            exclude(gender__exact=name.gender). \
            exclude(id__exact=name.id). \
            order_by('first')

    context = {
        'EditPCTitle': 'Edit Personal Contact: ' + name.first + ' ' + name.last,
        'addresses': addresses,
        'Admin': Z.Admin,
        'browser_tab': WZ['Tabs'][WZ['ActiveTab']][2],
        'form': form,
        'name': name,
        'nid': nid,
        'picture': WZ['httpURL'] + 'static/pics/names/default.jpg',
        'spouse': spouse,
        'schoices': schoices,
        'WZ': WZ
        }

    context.update(csrf(request))
    return render_to_response('DirectoryEditPC.html', context )

def donew(request, nid, browser_tab):
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    if nid != '0':
        try:
            name = Name.objects.get(pk=int(nid))
        except:
            return GoLogout(request, WZ, "[AN01]: URL containd an invalid name ID.")

        if WZ['Authority'] < Z.Admin and name.owner != WZ['AuthorizedOwner']:
            return GoLogout(request, WZ, "[AN02]: URL containd an invalid name ID.")

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditPCForm(request.POST, request.FILES)
        if form.is_valid():
            users = User.objects.all().filter(username__exact=form.cleaned_data['login_id'])
            if len(users) < 1:
                temporary_password = GenerateTemporaryPassword()

                new_user = User()
                new_user.username = 'pc' + str(time.time())
                new_user.first_name = form.cleaned_data['first_name']
                new_user.last_name = form.cleaned_data['last_name']
                new_user.email = name.Account_Email
                new_user.save()

                new_name = Name()
                new_name.user = new_user
                new_name.first = form.cleaned_data['first_name']
                new_name.last = form.cleaned_data['last_name']
                new_name.authority = Z.NewRO
                new_name.private = True
                new_name.owner = name.owner
                new_name.save()

                logger.info(WZ['User'] + ' AN ' + str(request.POST))

                return HttpResponseRedirect('/WhoZwho/ename/' + str(new_name.id) + '/' + browser_tab)
            else:
                WZ['ErrorMessage'] = "Error: The selected Login ID is already in use."
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        form = DirectoryEditPCForm()

    addresses = []
    schoices = []
    spouse = []

    context = {
        'EditPCTitle': 'Add a New Personal Contact',
        'Admin': Z.Admin,
        'addresses': addresses,
        'browser_tab': WZ['Tabs'][WZ['ActiveTab']][2],
        'form': form,
        'name': '',
        'nid': nid,
        'picture': WZ['httpURL'] + 'static/pics/names/default.jpg',
        'spouse': spouse,
        'schoices': schoices,
        'WZ': WZ
        }

    context.update(csrf(request))
    return render_to_response('DirectoryEditPC.html', context )
