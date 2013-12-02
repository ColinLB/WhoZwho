# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

import os
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

from models import Address, Name
from SessionFunctions import Kids, FamilyName, Parents, ProcessNewPicture 

class DirectoryEditNameForm(forms.Form):
    first = forms.CharField(max_length=32)
    last = forms.CharField(max_length=32)
    gender = forms.ChoiceField(widget=RadioSelect, choices=Z.Genders)
    Login_ID = forms.CharField(max_length=32)
    Account_Email = forms.EmailField(max_length=32)
    cell = forms.CharField(max_length=32, required=False)
    email = forms.EmailField(max_length=32, required=False)
    work_email = forms.EmailField(max_length=32, required=False)
    work_phone = forms.CharField(max_length=32, required=False)
    picture = forms.ImageField(required=False)
    birthday = DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year - 100, -1)), required=False)
    title = forms.ChoiceField(widget=Select, choices=Z.Titles, required=False)
    out_of_town = forms.BooleanField(required=False)

def do(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EN01]: URL contained an invalid name ID.")

    if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
        return GoLogout(request, ZS, "[EN02]: URL contained an invalid name ID.")

    if ZS['Authority'] >= Z.Admin:
        ZS['AuthorizedOwner'] = name.owner

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditNameForm(request.POST, request.FILES)
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
                if name.private == False:
                    name.out_of_town = form.cleaned_data['out_of_town']
                name.save()

                if name.user.username != form.cleaned_data['Login_ID'] or name.user.email != form.cleaned_data['Account_Email']:
                    if name.private == False:
                        name.user.username = form.cleaned_data['Login_ID']
                    name.user.email = form.cleaned_data['Account_Email']
                    name.user.save()

                logger.info(ZS['User'] + ' EN ' + str(request.POST))

                if request.FILES.has_key('picture'):
                    ZS['ErrorMessage'] = ProcessNewPicture(request, ZS, 'names', nid)

                # Check if the name has a picture and set indicator appropriately.
                if os.path.exists(ZS['StaticPath'] + 'pics/names/' + str(name.id) + '.jpg'):
                    if not name.picture_uploaded:
                        name.picture_uploaded = True
                        name.save()
                else:
                    if name.picture_uploaded:
                        name.picture_uploaded = False
                        name.save()

                if ZS['ErrorMessage'] == "":
                    if ZS['Authority'] >= Z.Admin:
                        return HttpResponseRedirect('/WhoZwho/aelst')
                    elif ZS['Authority'] >= Z.UserRW:
                        return HttpResponseRedirect('/WhoZwho/delst')
                    else:
                        return HttpResponseRedirect('/WhoZwho/wlist')
            else:
                ZS['ErrorMessage'] = "[EN03]: Login ID already used, choose another."
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        form = DirectoryEditNameForm(initial={
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
            'gender': name.gender,
            'out_of_town': name.out_of_town
            }) 

    if os.path.exists(ZS['StaticPath'] + 'pics/names/' + str(name.id) + '.jpg'):
        picture = ZS['httpURL'] + 'static/pics/names/' + str(name.id) + '.jpg'
    else:
        picture = ZS['httpURL'] + 'static/pics/defaults/greenman.gif'

    addresses = Address.objects.all(). \
        filter(owner__exact=ZS['AuthorizedOwner']). \
        order_by('street')

    context = {
        'addresses': addresses,
        'Admin': Z.Admin,
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'FamilyName': FamilyName(name),
        'form': form,
        'Kids': Kids(name),
        'name': name,
        'Parents': Parents(name),
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryEditName.html', context )
