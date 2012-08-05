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
from WhoZwhoCommonFunctions import GenerateTemporaryPassword

import captcha

class ForgotPasswordForm(forms.Form):
    login_id = forms.CharField(max_length=16)
    email = forms.EmailField(max_length=32)
    recaptcha_challenge_field = forms.CharField(widget=forms.Textarea)
    recaptcha_response_field = forms.CharField(max_length=128)

def do(request):
    WZ = Z.SetWhoZwho(request)
    if request.method == 'POST': # If the form has been submitted...
        form = ForgotPasswordForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            check_captcha = captcha.submit (form.cleaned_data['recaptcha_challenge_field'], form.cleaned_data['recaptcha_response_field'], WZ['CaptchaPrivate'], "127.0.0.1")
            if not check_captcha.is_valid:
                WZ['ErrorMessage'] = "[FP01]: Captcha response was incorrect."
            else:
                users = User.objects.all(). \
                    filter(username__exact=form.cleaned_data['login_id']). \
                    filter(email__exact=form.cleaned_data['email'])

                if len(users) == 1:
                    temporary_password = GenerateTemporaryPassword()

                    users[0].set_password(temporary_password)
                    users[0].save()

                    users[0].name.password_timeout = int(time())
                    users[0].name.save()

                    send_mail(
                        'Password Reset',
                        'A password reset request for your account has been received and a new ' + \
                        'temporary password has been assigned (see below). Visit ' + WZ['httpURL'] + '/login ' + \
                        'within the next 20 minutes and choose a new permanent password. If you need more ' + \
                        'time, you may visit ' + WZ['httpURL'] + '/fgpwd at any time to request another ' + \
                        'temporary password.\n\nLogin ID: ' + users[0].username + \
                        '\nTemporary password: ' + temporary_password,
                        'crlb@telus.net',
                        [users[0].email],
                        fail_silently=False)

                    WZ['ErrorMessage'] = "[FP02]: Temporary password sent to your email."
                else:
                    WZ['ErrorMessage'] = "[FP03]: Invalid Login ID/email."
        else:
            WZ['ErrorMessage'] = str(form.errors)
    else:
        form = ForgotPasswordForm()

    captcha_html = captcha.displayhtml(WZ['CaptchaPublic'], use_ssl = True)

    c = { 'form': form, 'WZ': WZ, 'captcha_html': captcha_html }
    c.update(csrf(request))
    return render_to_response('UserForgotPassword.html', c )
