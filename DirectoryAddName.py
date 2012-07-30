# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

import os.path
from django.forms.fields import ChoiceField
from django.forms.widgets import Select

from django import forms
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader

from models import Name
from WhoZwhoCommonFunctions import GenerateTemporaryPassword

class DirectoryAddNameForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=32)
    login_id = forms.CharField(max_length=16)
    privileges = forms.ChoiceField(widget=Select, choices=Z.Privileges)

def do(request, nid, browser_tab):
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
        form = DirectoryAddNameForm(request.POST, request.FILES)
        if form.is_valid():
            users = User.objects.all().filter(username__exact=form.cleaned_data['login_id'])
            if len(users) < 1:
                temporary_password = GenerateTemporaryPassword()

                new_user = User()
                new_user.username = form.cleaned_data['login_id']
                new_user.first_name = form.cleaned_data['first_name']
                new_user.last_name = form.cleaned_data['last_name']
                new_user.email = form.cleaned_data['email']
                new_user.set_password(temporary_password)
                new_user.save()

                new_name = Name()
                new_name.user = new_user
                new_name.first = form.cleaned_data['first_name']
                new_name.last = form.cleaned_data['last_name']

                if form.cleaned_data['privileges'] == '1':
                    new_name.authority = Z.NewRO
                else:
                    new_name.authority = Z.NewRW

                if nid != '0':
                    new_name.owner = name.owner

                new_name.save()

                if nid == '0':
                    new_name.owner = new_name.id
                    new_name.save()

                logger.info(WZ['User'] + ' AN ' + str(request.POST))

                send_mail(
                    'Your new WhoZwho directory account.',
                    'A new account, ' + new_user.username + \
                    ', has been created for you on the WhoZwho directory. ' + \
                    'To obtain a password, visit ' + WZ['httpURL'] + '/fgpwd.',
                    'crlb@telus.net',
                    [new_user.email],
                    fail_silently=False)

                return HttpResponseRedirect('/WhoZwho/ename/' + str(new_name.id) + '/' + browser_tab)
            else:
                WZ['ErrorMessage'] = "Error: The selected Login ID is already in use."
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        form = DirectoryAddNameForm(initial={
            'privileges': str(Z.NewRW),
            }) 

    if nid == '0':
        AddNameTitle = 'Add a New Name'
    else:
        AddNameTitle = 'Add a New Family Member'

    context = {
        'AddNameTitle': AddNameTitle,
        'browser_tab': WZ['Tabs'][WZ['ActiveTab']][2],
        'form': form,
        'nid': nid,
        'WZ': WZ
        }

    context.update(csrf(request))
    return render_to_response('DirectoryAddName.html', context )
