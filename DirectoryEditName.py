# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import logging
logger = logging.getLogger('WhoZwho.update')

import os
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

from models import Address, Name, Wedding
from SessionFunctions import SaveFileUpload

class DirectoryEditNameForm(forms.Form):
    first = forms.CharField(max_length=32)
    last = forms.CharField(max_length=32)
    Login_ID = forms.CharField(max_length=32)
    Account_Email = forms.EmailField(max_length=32)
    cell = forms.CharField(max_length=32, required=False)
    email = forms.EmailField(max_length=32, required=False)
    work_email = forms.EmailField(max_length=32, required=False)
    work_phone = forms.CharField(max_length=32, required=False)
    picture = forms.ImageField(required=False)
    birthday = DateField(widget=SelectDateWidget(years=range(date.today().year, date.today().year - 100, -1)), required=False)
    title = forms.ChoiceField(widget=Select, choices=Z.Titles, required=False)
    gender = forms.ChoiceField(widget=RadioSelect, choices=Z.Genders)

def do(request, nid, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS)

    try:
        name = Name.objects.get(pk=int(nid))
    except:
        return GoLogout(request, ZS, "[EN01]: URL contained an invalid name ID.")

    if ZS['Authority'] < Z.Admin and name.owner != ZS['AuthorizedOwner']:
        return GoLogout(request, ZS, "[EN02]: URL contained an invalid name ID.")

    if ZS['Authority'] >= Z.Admin:
        ZS['AuthorizedOwner'] = name.owner

    if request.method == 'POST': # If the form has been submitted...
        form = DirectoryEditNameForm(request.POST, request.FILES)
        if form.is_valid():
            users = User.objects.all().filter(username__exact=form.cleaned_data['Login_ID']).exclude(id__exact=name.user.id)
            if len(users) < 1:
                name.first = form.cleaned_data['first']
                name.last = form.cleaned_data['last']
                name.email = form.cleaned_data['email']
                name.cell = form.cleaned_data['cell']
                name.work_email = form.cleaned_data['work_email']
                name.work_phone = form.cleaned_data['work_phone']
                name.birthday = form.cleaned_data['birthday']
                name.title = form.cleaned_data['title']
                name.gender = form.cleaned_data['gender']
                name.save()

                if name.user.username != form.cleaned_data['Login_ID'] or name.user.email != form.cleaned_data['Account_Email']:
                    name.user.username = form.cleaned_data['Login_ID']
                    name.user.email = form.cleaned_data['Account_Email']
                    name.user.save()

                logger.info(ZS['User'] + ' EN ' + str(request.POST))

                if request.FILES.has_key('picture'):
                    ZS['ErrorMessage'] = ProcessNewPicture(request, ZS, nid)

                if ZS['ErrorMessage'] == "":
                    if ZS['Authority'] >= Z.Admin:
                        return HttpResponseRedirect('/WhoZwho/aelst')
                    elif ZS['Authority'] >= Z.UserRW:
                        return HttpResponseRedirect('/WhoZwho/delst')
                    else:
                        return HttpResponseRedirect('/WhoZwho/wlist')
            else:
                ZS['ErrorMessage'] = "[EN03]: Login ID already used, choose another."
        else:
            ZS['ErrorMessage'] = str(form.errors)
    else:
        form = DirectoryEditNameForm(initial={
            'Login_ID': name.user.username,
            'first': name.first,
            'last': name.last,
            'email': name.email,
            'cell': name.cell,
            'work_email': name.work_email,
            'work_phone': name.work_phone,
            'Account_Email': name.user.email,
            'birthday': name.birthday,
            'title': name.title,
            'gender': name.gender
            }) 

    if os.path.exists(ZS['StaticPath'] + 'pics/names/' + str(name.id) + '.jpg'):
        picture = ZS['httpURL'] + 'static/pics/names/' + str(name.id) + '.jpg'
    else:
        picture = ZS['httpURL'] + 'static/pics/defaults/greenman.gif'

    addresses = Address.objects.all(). \
        filter(owner__exact=ZS['AuthorizedOwner']). \
        order_by('street')

    if name.wedding:
        spouse = name.wedding.name_set.all(). \
            exclude(id__exact=name.id)
        schoices = []
    else:
        spouse = []
        schoices = Name.objects.all(). \
            filter(owner__exact=ZS['AuthorizedOwner']). \
            filter(wedding__exact=None). \
            exclude(gender__exact=name.gender). \
            exclude(id__exact=name.id). \
            order_by('first')

    context = {
        'addresses': addresses,
        'Admin': Z.Admin,
        'browser_tab': ZS['Tabs'][ZS['ActiveTab']][2],
        'form': form,
        'name': name,
        'nid': nid,
        'picture': picture,
        'spouse': spouse,
        'schoices': schoices,
        'ZS': ZS
        }

    context.update(csrf(request))
    return render_to_response('DirectoryEditName.html', context )

def ProcessNewPicture(request, ZS, nid):
    std_jpg_size = Z.jpg_width * Z.jpg_height
    std_jpg_width_height_ratio = Z.jpg_width * 1.0 / Z.jpg_height

    os.environ['PATH'] = ZS['PythonPath']

    SaveFileUpload(request.FILES['picture'], ZS['StaticPath'] + 'pics/new_names/' + nid +'.jpg')

    # Retrieve image information and check image type.
    p = Popen(['identify', ZS['StaticPath'] + 'pics/new_names/' + nid +'.jpg'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stderr != '':
        return  "[EN04]: /usr/bin/identify error - " + stderr

    file_info = stdout.split()
    if file_info[1] != 'JPEG':
        p = Popen(['rm', '-f',  ZS['StaticPath'] + 'pics/new_names/' + nid +'.jpg'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if stderr != '':
            return  "[EN05]: /bin/rm error - " + stderr

        return  "[EN06]: Picture rejected; only JPEGs allowed."

    file_dimensions = file_info[2].split('x')
    raw_width = int(file_dimensions[0])
    raw_height = int(file_dimensions[1])

    # Scale the image if necessary.
    if raw_width * raw_height > std_jpg_size:
        normalized_height = 0
        if int(raw_width / std_jpg_width_height_ratio) > raw_height:
            if raw_height > Z.jpg_height:
                normalized_height = Z.jpg_height
                normalized_width = int(raw_width * Z.jpg_height / raw_height)
        else:
            if raw_width > Z.jpg_width:
                normalized_height = int(raw_height * Z.jpg_width / raw_width)
                normalized_width = Z.jpg_width

        if normalized_height > 0:
            p = Popen(['mogrify', '-scale',
                str(normalized_width) + 'x' + str(normalized_height),
                ZS['StaticPath'] + 'pics/new_names/' + nid +'.jpg'],
                stdout=PIPE, stderr=PIPE)

            stdout, stderr = p.communicate()
            if stderr != '':
                return  "[EN07]: /usr/bin/mogrify(scale) error - " + stderr

            raw_width = normalized_width
            raw_height = normalized_height

    # Crop the image if necessary.
    normalized_height = 0
    raw_ratio = raw_width * 1.0 / raw_height
    if raw_ratio > Z.jpg_crop_width_threshold:
        normalized_height = raw_height
        normalized_height_offset = 0
        normalized_width = int(raw_height * std_jpg_width_height_ratio)
        normalized_width_offset = int((raw_width - normalized_width) / 2)

    elif raw_ratio < Z.jpg_crop_height_threshold:
        normalized_height = int(raw_width / std_jpg_width_height_ratio)
        normalized_height_offset = int((raw_height - normalized_height) / 2)
        normalized_width = raw_width
        normalized_width_offset = 0

    if normalized_height > 0:
        p = Popen(['mogrify', '-crop',
            str(normalized_width) + 'x' + str(normalized_height) + '+' + str(normalized_width_offset) + '+' + str(normalized_height_offset),
            ZS['StaticPath'] + 'pics/new_names/' + nid +'.jpg'],
            stdout=PIPE, stderr=PIPE)

        stdout, stderr = p.communicate()
        if stderr != '':
            return  "[EN08]: /usr/bin/mogrify(crop) error - " + stderr

    # Still alive? Move the image into production.
    p = Popen(['mv',
        ZS['StaticPath'] + 'pics/new_names/' + nid +'.jpg',
        ZS['StaticPath'] + 'pics/names/' + nid +'.jpg'],
        stdout=PIPE, stderr=PIPE)

    stdout, stderr = p.communicate()
    if stderr != '':
        return  "[EN09]: /bin/mv error - " + stderr

    logger.info(ZS['User'] + ' EN ' + str(request.FILES))

    return ''
