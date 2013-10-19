# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

from time import time
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from models import Name

import captcha

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=32)
    login_id = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)
    vpassword = forms.CharField(max_length=16, widget=forms.PasswordInput)
    recaptcha_challenge_field = forms.CharField(widget=forms.Textarea)
    recaptcha_response_field = forms.CharField(max_length=128)

def now(request):
    ZS = Z.SetWhoZwho(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid(): 
            check_captcha = captcha.submit (form.cleaned_data['recaptcha_challenge_field'], form.cleaned_data['recaptcha_response_field'], ZS['CaptchaPrivate'], "127.0.0.1")
            if not check_captcha.is_valid:
                ZS['ErrorMessage'] = "[UR01]: Captcha response was incorrect."
            else:
                users = User.objects.all().filter(username__exact=form.cleaned_data['login_id'])
                if len(users) < 1:
                    new_user = User()
                    new_user.username = form.cleaned_data['login_id']
                    new_user.first_name = form.cleaned_data['first_name']
                    new_user.last_name = form.cleaned_data['last_name']
                    new_user.email = form.cleaned_data['email']
                    new_user.set_password(form.cleaned_data['password'])
                    new_user.save()

                    new_name = Name()
                    new_name.preferred = form.cleaned_data['first_name']
                    new_name.first = form.cleaned_data['first_name']
                    new_name.last = form.cleaned_data['last_name']
                    new_name.authority = Z.NewRW
                    new_name.user = new_user
                    new_name.save()

                    new_name.owner = new_name.id
                    new_name.save()

                    auth_user = authenticate(username=new_user, password=form.cleaned_data['password'])
                    if auth_user is not None:
                        if auth_user.is_active:
                            login(request, auth_user)
                            ZS['Authenticated'] = 1
                            request.session['last_time'] = time()
                            ZS = Z.SetWhoZwho(request, '.')
                            return HttpResponseRedirect('/WhoZwho/' + ZS['Tabs'][ZS['ActiveTab']][3])
                        else:
                            ZS['ErrorMessage'] = "[UR02]: Login ID disabled."
                    else:
                        ZS['ErrorMessage'] = "[UR03]: Login ID is invalid."
                else:
                    ZS['ErrorMessage'] = "[UR04]: The selected Login ID is already in use."
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        form = RegistrationForm() # An unbound form

    captcha_html = captcha.displayhtml(ZS['CaptchaPublic'], use_ssl = True)

    c = { 'form': form, 'ZS': ZS, 'captcha_html': captcha_html }
    c.update(csrf(request))
    return render_to_response('UserRegistration.html', c )
