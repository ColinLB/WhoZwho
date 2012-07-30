# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
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
from WhoZwhoCommonFunctions import GenerateTemporaryPassword

import captcha

class UserChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)
    vpassword = forms.CharField(max_length=16, widget=forms.PasswordInput)
    recaptcha_challenge_field = forms.CharField(widget=forms.Textarea)
    recaptcha_response_field = forms.CharField(max_length=128)

def do(request):
    WZ = Z.SetWhoZwho(request)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ)

    if request.method == 'POST': # If the form has been submitted...
        form = UserChangePasswordForm(request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            check_captcha = captcha.submit (form.cleaned_data['recaptcha_challenge_field'], form.cleaned_data['recaptcha_response_field'], Z.captcha_private_key, "127.0.0.1")
            if not check_captcha.is_valid:
                WZ['ErrorMessage'] = "[CP01]: Captcha response was incorrect."
            else:
                try:
                    user = User.objects.get(username__exact=WZ['User'])
                except:
                    return GoLogout(request, WZ, "[CP02]: Password change disabled.")

 
                user.set_password(form.cleaned_data['password'])
                user.save()

                user.name.password_timeout = None
                user.name.save()

                auth_user = authenticate(username=WZ['User'], password=form.cleaned_data['password'])
                if auth_user is not None:
                    if auth_user.is_active:
                        login(request, auth_user)
                        WZ['Authenticated'] = 1
                        request.session['last_time'] = time()
                        WZ = Z.SetWhoZwho(request, '.')
                        return HttpResponseRedirect('/WhoZwho/' + WZ['Tabs'][WZ['ActiveTab']][3])
                    else:
                        WZ['ErrorMessage'] = "[CP03]: Login ID disabled."
                else:
                    WZ['ErrorMessage'] = "[CP04]: Login ID disabled."
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        form = UserChangePasswordForm()

    captcha_html = captcha.displayhtml(Z.captcha_public_key, use_ssl = True)

    context = {
        'captcha_html': captcha_html,
        'form': form,
        'WZ': WZ
        }

    context.update(csrf(request))
    return render_to_response('UserChangePassword.html', context )
