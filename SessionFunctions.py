# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import logging
logger = logging.getLogger('WhoZwho.update')

from django.db.models import Q
from models import Family, Name
from subprocess import PIPE, Popen, STDOUT
import SessionSettings as Z
import os
import string
import random
import datetime

def Age(bday=None, d=None):
    if bday is None:
        return 1000
    if d is None:
        d = datetime.date.today()

    return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))

def Birthday(name):
    try:
        return Z.Months[name.birthday.month - 1] + ', ' + str(name.birthday.day)
    except:
        return ""

def FamilyAddress(name, prefix=''):
    contact_array = []

    if name.family:
        if name.family.email:
            contact_array += [ name.family.email ]

        if name.family.spouses.count() == 2:
            spouses = name.family.spouses.all()
            if spouses[0].address and spouses[1].address:
                if spouses[0].gender == 'm':
                    address = spouses[0].address
                else:
                    address = spouses[1].address
            elif spouses[0].address:
                address = spouses[0].address
            elif spouses[1].address:
                address = spouses[1].address
            else:
                address = None
        else:
            address = name.address
    else:
        address = name.address

    if address:
        if address.phone:
            contact_array += [ address.phone ]

        address_array = [ prefix + address.street, prefix + address.city + ', ' + address.province + ', ' + address.postcode ]

        if len(contact_array) > 0:
            address_array += [ prefix + ', '.join(contact_array) ]
    else:
        address_array = []

    return address_array

def FamilyName(name,opt='lastfirst', prefix=''):
    if name.family:
        spouses = name.family.spouses.all()
        if len(spouses) < 2:
            if opt == 'lastfirst':
                return prefix +  name.last + ", " + name.first
            else:
                return prefix +  name.first + " " + name.last
        else:
            if spouses[0].gender == 'm':
                if opt == 'lastfirst':
                    return prefix +  spouses[0].last + ", " + spouses[0].first + " & " + spouses[1].first
                else:
                    return prefix +  spouses[0].first + " & " + spouses[1].first + ' ' + spouses[0].last
            else:
                if opt == 'lastfirst':
                    return prefix +  spouses[1].last + ", " + spouses[1].first + " & " + spouses[0].first
                else:
                    return prefix +  spouses[1].first + " & " + spouses[0].first + ' ' + spouses[1].last

    return PersonalName(name, opt, prefix)

def FormatAddress(address, prefix=''):
    if address:
        address_array = [ prefix + address.street ]

        if address.address_line2:
            address_array += [ address.address_line2 ]

        if address.address_line3:
            address_array += [ address.address_line3 ]

        address_array += [ prefix + address.city + ', ' + address.province + ', ' + address.postcode ]

        contact_array = []
        if address.email:
            contact_array += [ address.email ]

        if address.phone:
            contact_array += [ address.phone ]


        if len(contact_array) > 0:
            address_array += [ prefix + ', '.join(contact_array) ]
    else:
        address_array = []

    return address_array


def GenerateTemporaryPassword(size=7, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def GetDirectoryLists(ZS):
    names = Name.objects.all(). \
        exclude(Q(private__exact=True) & ~Q(owner__exact=ZS['AuthorizedOwner'])). \
        exclude(removed__exact=True). \
        exclude(approved__exact=False). \
        exclude(last__isnull=True). \
        exclude(last__exact=''). \
        order_by('last', 'first')

    church_list = []
    friend_list = []
    for name in names:
        if name.out_of_town or name.private == True:
            friend_list += [name]
        else:
            church_list += [name]

    return [ church_list, friend_list ]

def PersonalContacts(name):
    array_1 = []
    if not name:
        return array_1

    array_2 = []
    if name.email:
        array_2 += [ name.email ]

    if name.cell:
        array_2 += [ name.cell ]

    if len(array_2) > 0:
        array_1 += [ 'Personal: ' + ', '.join(array_2) ]

    array_2 = []
    if name.work_email:
        array_2 += [ name.work_email ]

    if name.work_phone:
        array_2 += [ name.work_phone ]

    if len(array_2) > 0:
        array_1 += [ 'Work: ' + ', '.join(array_2) ]

    return array_1

def PersonalName(name,opt='firstlast', prefix=''):
    if opt == 'lastfirst':
        return prefix +  name.last + ", " + name.first
    else:
        return prefix +  name.first + " " + name.last

def Kids(name, prefix=''):
    kids = []
    if name.family:
        children = name.family.children.all().order_by('birthday')
        for child in children:
            if Age(child.birthday) < 18:
                kids += [child.first]

    if len(kids) > 0:
        return [ prefix + ', '.join(kids) ]

    return []

def NameContacts(name, prefix=''):
    contacts = []
    if name.email:
        contacts += [ name.email ]
    if name.cell:
        contacts += [ name.cell ]
    if name.work_email:
        contacts += [ name.work_email ]
    if name.work_phone:
        contacts += [ name.work_phone ]

    if len(contacts) > 0:
        return prefix +  name.first + ': ' + ', '.join(contacts)
    else:
        return  ''

def Parents(name):
    if name.parents:
        return [ FamilyName(name.parents.spouses.all()[0], 'firstlast') ]

    return []

def ProcessNewPicture(request, ZS, pic_dir, nid):
    std_jpg_size = Z.jpg_width * Z.jpg_height
    std_jpg_width_height_ratio = Z.jpg_width * 1.0 / Z.jpg_height

    os.environ['PATH'] = ZS['PythonPath']

    SaveFileUpload(request.FILES['picture'], ZS['StaticPath'] + 'pics/staging/' + pic_dir + '_' + nid +'.jpg')

    # Retrieve image information and check image type.
    p = Popen(['identify', ZS['StaticPath'] + 'pics/staging/' + pic_dir + '_' + nid +'.jpg'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stderr != '':
        return  "[EN04]: /usr/bin/identify error - " + stderr

    file_info = stdout.split()
    if file_info[1] != 'JPEG':
        p = Popen(['rm', '-f',  ZS['StaticPath'] + 'pics/staging/' + pic_dir + '_' + nid +'.jpg'], stdout=PIPE, stderr=PIPE)
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
                ZS['StaticPath'] + 'pics/staging/' + pic_dir + '_' + nid +'.jpg'],
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
            ZS['StaticPath'] + 'pics/staging/' + pic_dir + '_' + nid +'.jpg'],
            stdout=PIPE, stderr=PIPE)

        stdout, stderr = p.communicate()
        if stderr != '':
            return  "[EN08]: /usr/bin/mogrify(crop) error - " + stderr

    # Still alive? Move the image into production.
    p = Popen(['mv',
        ZS['StaticPath'] + 'pics/staging/' + pic_dir + '_' + nid +'.jpg',
        ZS['StaticPath'] + 'pics/' + pic_dir + '/' + nid +'.jpg'],
        stdout=PIPE, stderr=PIPE)

    stdout, stderr = p.communicate()
    if stderr != '':
        return  "[EN09]: /bin/mv error - " + stderr

    logger.info(ZS['User'] + ' EN ' + str(request.FILES))

    return ''

def SaveFileUpload(infile, outfile):
    destination = open(outfile, 'wb+')
    for chunk in infile.chunks():
        destination.write(chunk)
    destination.close()
