# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import logging
logger = logging.getLogger('WhoZwho.update')

from django.db.models import Q
from models import Name
from subprocess import PIPE, Popen, STDOUT
import SessionSettings as Z
import os
import string
import random

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
