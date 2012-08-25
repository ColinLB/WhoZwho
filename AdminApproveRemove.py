# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
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

class AdminApproveRemoveForm(forms.Form):
    action = forms.CharField()

def do(request, nid):
    WZ = Z.SetWhoZwho(request, 'Admin')
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ, '')

    name = Name.objects.get(pk=int(nid))

    if request.method == 'POST': # If the form has been submitted...
        form = AdminApproveRemoveForm(request.POST)
        if form.is_valid():

            logger.info(WZ['User'] + ' AA ' + str(request.POST))

            if form.cleaned_data['action'] == 'a':
                name.approved = True
                name.save()

                send_mail(
                    'Account approved.',
                    'Your Login ID, ' + name.user.username + ', has been approved. Visit ' + \
                    WZ['httpURL'] + '/login to access the WhoZwho directory.',
                    WZ['AdminEmail'],
                    [name.user.email],
                    fail_silently=False)

                return HttpResponseRedirect('/WhoZwho/alist')

            elif form.cleaned_data['action'] == 'r':
                name.removed = True
                name.save()
                return HttpResponseRedirect('/WhoZwho/alist')
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        form = AdminApproveRemoveForm(initial={ 'action': "" }) 

    if os.path.exists(WZ['StaticPath'] + 'pics/names/' + str(name.id) + '.jpg'):
        picture = WZ['httpURL'] + 'static/pics/names/' + str(name.id) + '.jpg'
    else:
        picture = WZ['httpURL'] + 'static/pics/defaults/greenman.gif'

    context = {
        'browser_tab': WZ['Tabs'][WZ['ActiveTab']][2],
        'form': form,
        'name': name,
        'nid': nid,
        'picture': picture,
        'WZ': WZ
        }

    context.update(csrf(request))
    return render_to_response('AdminApproveRemove.html', context )
