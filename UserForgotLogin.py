# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z

from time import time
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from models import Name
import captcha

class ForgotLoginForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=32)
    recaptcha_challenge_field = forms.CharField(widget=forms.Textarea)
    recaptcha_response_field = forms.CharField(max_length=128)

def do(request):
    WZ = Z.SetWhoZwho(request)
    if request.method == 'POST': # If the form has been submitted...
        form = ForgotLoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            check_captcha = captcha.submit (form.cleaned_data['recaptcha_challenge_field'], form.cleaned_data['recaptcha_response_field'], WZ['CaptchaPrivate'], "127.0.0.1")
            if not check_captcha.is_valid:
                WZ['ErrorMessage'] = "[FL01]: Captcha response was incorrect."
            else:
                users = User.objects.all(). \
                    filter(first_name__exact=form.cleaned_data['first_name']). \
                    filter(last_name__exact=form.cleaned_data['last_name']). \
                    filter(email__exact=form.cleaned_data['email'])

                if len(users) == 1:
                    send_mail(
                        'Forgotten login ID.',
                        'Login ID: ' + users[0].username,
                        WZ['AdminEmail'],
                        [users[0].email],
                        fail_silently=False)

                    WZ['ErrorMessage'] = "[FL02]: Login ID sent to your email."
                else:
                    WZ['ErrorMessage'] = "[FL03]: Invalid Login ID."
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        form = ForgotLoginForm()

    captcha_html = captcha.displayhtml(WZ['CaptchaPublic'], use_ssl = True)

    c = { 'form': form, 'WZ': WZ, 'captcha_html': captcha_html }
    c.update(csrf(request))
    return render_to_response('UserForgotLogin.html', c )
