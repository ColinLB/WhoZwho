# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import os.path
from django.forms.fields import ChoiceField, DateField
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Select, RadioSelect

from time import time
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader

from models import Address, Name
from SessionFunctions import GenerateTemporaryPassword

class UserChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)
    vpassword = forms.CharField(max_length=16, widget=forms.PasswordInput)

def do(request, browser_tab):
    ZS = Z.SetWhoZwho(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    if request.method == 'POST': # If the form has been submitted...
        form = UserChangePasswordForm(request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            try:
                user = User.objects.get(username__exact=ZS['User'])
            except:
                return GoLogout(request, ZS, "[CP02]: Password change disabled.")


            user.set_password(form.cleaned_data['password'])
            user.save()

            user.name.password_timeout = None
            user.name.save()

            auth_user = authenticate(username=ZS['User'], password=form.cleaned_data['password'])
            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)
                    ZS['Authenticated'] = 1
                    request.session['last_time'] = time()
                    ZS = Z.SetWhoZwho(request, '.')
                    return HttpResponseRedirect('/WhoZwho/' + ZS['Tabs'][ZS['ActiveTab']][3])
                else:
                    ZS['ErrorMessage'] = "[CP03]: Login ID disabled."
            else:
                ZS['ErrorMessage'] = "[CP04]: Login ID disabled."
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        form = UserChangePasswordForm()

    context = {
        'browser_tab': browser_tab,
        'form': form,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('UserChangePassword.html', context )
