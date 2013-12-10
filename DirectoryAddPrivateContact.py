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

from models import Name
from SessionFunctions import SaveFileUpload

class AddPrivateContactForm(forms.Form):
    first = forms.CharField(max_length=32)
    last = forms.CharField(max_length=32)
    gender = forms.ChoiceField(widget=RadioSelect, choices=Z.Genders)

def do(request, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    if request.method == 'POST': # If the form has been submitted...
        form = AddPrivateContactForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = User.objects.get(username__exact=ZS['User'])
            except:
                return GoLogout(request, ZS, "[PC01]: Add private contact disabled.")

            new_user = User()
            new_user.username = 'pc' + str(time.time())
            new_user.first_name = form.cleaned_data['first']
            new_user.last_name = form.cleaned_data['last']
            new_user.email = user.email
            new_user.save()

            new_name = Name()
            new_name.user = new_user
            new_name.approved = True
            new_name.authority = Z.NewRO
            new_name.private = True
            new_name.owner = user.name.owner

            new_name.first = form.cleaned_data['first']
            new_name.last = form.cleaned_data['last']
            new_name.gender = form.cleaned_data['gender']
            new_name.save()

            logger.info(ZS['User'] + ' PC ' + str(request.POST))

            return HttpResponseRedirect('/WhoZwho/ename/' + str(new_name.id) + '/' + browser_tab)
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        form = AddPrivateContactForm()

    context = {
        'Admin': Z.Admin,
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryAddPrivateContact.html', context )
