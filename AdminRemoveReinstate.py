# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

import os.path
from django import forms
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader
from models import Name

import DirectoryDeleteByName

class AdminRemoveReinstateForm(forms.Form):
    action = forms.CharField()

def do(request, nid):
    ZS = Z.SetWhoZwho(request, 'Admin')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    name = Name.objects.get(pk=int(nid))

    if request.method == 'POST': # If the form has been submitted...
        form = AdminRemoveReinstateForm(request.POST)
        if form.is_valid():

            logger.info(ZS['User'] + ' AI ' + str(request.POST))

            if form.cleaned_data['action'] == 'i':
                name.removed = False
                name.save()
            elif form.cleaned_data['action'] == 'p':
                DirectoryDeleteByName.do(request, nid, 'Admin')

            return HttpResponseRedirect('/WhoZwho/rilst')
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        form = AdminRemoveReinstateForm(initial={ 'action': "" }) 

    if os.path.exists(ZS['StaticPath'] + 'pics/names/' + str(name.id) + '.jpg'):
        picture = ZS['httpURL'] + 'static/pics/names/' + str(name.id) + '.jpg'
    else:
        picture = ZS['httpURL'] + 'static/pics/defaults/greenman.gif'

    context = {
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'name': name,
        'nid': nid,
        'picture': picture,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('AdminRemoveReinstate.html', context )

def dorm(request, nid):
    ZS = Z.SetWhoZwho(request, 'Admin')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    name = Name.objects.get(pk=int(nid))

    name.removed = True
    name.save()

    return HttpResponseRedirect('/WhoZwho/aelst')
