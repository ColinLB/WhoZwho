# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z

from time import time
from django import forms
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

import logging
logger = logging.getLogger('WhoZwho.update')

from models import Name

class LoginForm(forms.Form):
    login_id = forms.CharField(max_length=16)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)

def do(request):
    ZS = Z.SetSession(request)
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            auth_user = authenticate(username=form.cleaned_data['login_id'], password=form.cleaned_data['password'])
            if auth_user is not None:
                if auth_user.name.bad_password_timeout:
                    temp_bad_password_timeout = auth_user.name.bad_password_timeout + Z.BadPasswordTimeout
                else:
                    temp_bad_password_timeout = Z.BadPasswordTimeout

                if time() < temp_bad_password_timeout:
                    auth_user.name.bad_password_timeout = time()
                    auth_user.name.save()
                    ZS['ErrorMessage'] = "[UL01]: The login ID or password is invalid."
                elif auth_user.name.removed == True:
                    ZS['ErrorMessage'] = "[UL02]: The login ID or password is invalid."
                else:
                    if auth_user.is_active:
                        login(request, auth_user)
                        ZS['Authenticated'] = 1
                        request.session['last_time'] = time()

                        ZS = Z.SetSession(request, '.')

                        if ZS['TemporaryPasswordTimestamp'] > 0:
                            if ZS['TemporaryPasswordTimestamp'] < int(time()) - Z.TemporaryPasswordLife:
                                auth.logout(request)
                                ZS['Authenticated'] = 0
                                ZS['ErrorMessage'] = "[UL03]: Your temporary password has expired."
                            else:
				logger.info(ZS['User'] + ' (' + request.META['REMOTE_ADDR'] + ') logged in, authority ' + str(ZS['Authority']) + ', change password.')
                                return HttpResponseRedirect('/WhoZwho/chpwd/None')
                        else:
                            logger.info(ZS['User'] + ' (' + request.META['REMOTE_ADDR'] + ') logged in, authority ' + str(ZS['Authority']) + '.')
                            return HttpResponseRedirect('/WhoZwho/' + ZS['Tabs'][ZS['ActiveTab']][3])
                    else:
                        ZS['ErrorMessage'] = "[UL04]: The login ID or password is invalid."
            else:
                # Increment bad passwords
                try:
                    unauth_user = User.objects.get(username__exact=form.cleaned_data['login_id'])
                    if unauth_user.name.bad_password_timeout:
                        temp_bad_password_timeout = unauth_user.name.bad_password_timeout + Z.BadPasswordTimeout
                    else:
                        temp_bad_password_timeout = Z.BadPasswordTimeout

                    if time() < temp_bad_password_timeout:
                        unauth_user.name.bad_password_timeout = time()
                        unauth_user.name.save()
                    elif unauth_user.name.bad_password_attempts:
                        unauth_user.name.bad_password_attempts += 1
                    else:
                        unauth_user.name.bad_password_attempts = 1

                    if unauth_user.name.bad_password_attempts >= Z.BadPasswordAttempts:
                        unauth_user.name.bad_password_attempts = None
                        unauth_user.name.bad_password_timeout = time()

                    unauth_user.name.save()
                except:
                    pass

                ZS['ErrorMessage'] = "[UL05]: The login ID or password is invalid."
        else:
            ZS['ErrorMessage'] = "[UL06]: The login ID or password is invalid."
    else:
        form = LoginForm() # An unbound form
        ZS['ErrorMessage'] = ""

    c = { 'form': form, 'ZS': ZS }
    c.update(csrf(request))
    return render_to_response('UserLogin.html', c )

def GoLogout(request, ZS, error_message=''):
    auth.logout(request)
    ZS['Authenticated'] = 0

    if error_message:
        ZS['ErrorMessage'] = error_message

    form = LoginForm()

    c = { 'form': form, 'ZS': ZS }
    c.update(csrf(request))
    response = render_to_response('UserLogin.html', c )
    response.set_cookie('dlist_parm', 'F..')
    return response
