# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import esquimalt.settings

#
# Privileges and Authority Levels.
#
ApprovedOffset = 10
NewRO = 1
NewRW = 2
Admin = 3 + ApprovedOffset
UserRO = NewRO + ApprovedOffset
UserRW = NewRW + ApprovedOffset

Privileges = (
    ('1', 'Cannot Update Family'),
    ('2', 'Can Update Family')
    )

#
# Timeout periods (seconds) and counts.
#
BadPasswordAttempts = 5
BadPasswordTimeout = 3600
MaximumInactivity = 300
TemporaryPasswordLife = 1200

#
# Standard picture sizes.
#
jpg_height = 1000
jpg_width = 800
jpg_crop_height_threshold = 0.7
jpg_crop_width_threshold = 0.9

#
# Gender choices.
#
Genders = (
    ('m', 'Male'),
    ('f', 'Female')
    )

#
# Months.
#
Months = (
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
    )

#
# Salutations.
#
Titles = (
    ('0', 'Mr.'),
    ('1', 'Mrs.'),
    ('2', 'Master'),
    ('3', 'Miss'),
    ('4', 'Ms.'),
    ('5', 'Dr.'),
    ('6', 'Prof.'),
    ('7', 'Rev.'),
    )

from os import getcwd
from time import time
from django.contrib.auth.models import User

def SetSession(request, active_tab='None'):
    ZS = {
        'ActiveTab': 0,
        'AdminEmail': esquimalt.settings.ADMINS[0][1],
        'Approved': 0,
        'Authenticated': 0,
        'Authority': 0,
        'AuthorizedOwner': 0,
        'Banner': esquimalt.settings.BANNER,
        'BrowserTag': 'WhoZwho',
        'CaptchaPrivate': esquimalt.settings.CAPTCHA_PRIVATE_KEY,
        'CaptchaPublic': esquimalt.settings.CAPTCHA_PUBLIC_KEY,
        'ErrorMessage': '',
        'httpURL': 'https://' + request.META['HTTP_HOST'] + '/WhoZwho/',
        'InitializeBody': 0,
        'Nid': request.user.id,
        'PythonPath': esquimalt.settings.PYTHON_PATH,
        'StaticPath': getcwd() + '/django/' + esquimalt.settings.SITENAME + '/WhoZwho/static/',
        'Tab': {},
        'Tabs': [],
        'TemporaryPasswordTimestamp': 0,
        'UpdateLogFN': esquimalt.settings.LOGGING['handlers']['write_log']['filename'],
        'User': request.user.username,
        }

    if request.user.is_authenticated():
        try:
            last_time = request.session['last_time']
        except:
            last_time = 0

        now = time()
        if (now - last_time) < MaximumInactivity:
            ZS['Authenticated'] = 1
            request.session['last_time'] = now
        else:
            ZS['ErrorMessage'] = '[WW01]: Login timed out after 5 minutes of inactivity.'
            return ZS

    if active_tab == 'None':
        return ZS

    if not ZS['Authenticated']:
        ZS['ErrorMessage'] = '[WW02]: You are not logged in.'
        return ZS

    try:
        user = User.objects.get(username__exact=ZS['User'])
        if user.name.password_timeout:
            ZS['TemporaryPasswordTimestamp'] = user.name.password_timeout
            return ZS

        ZS['Approved'] = user.name.approved
        ZS['Authority'] = user.name.authority + ( ApprovedOffset * user.name.approved )
        ZS['AuthorizedOwner'] = user.name.owner
    except:
        return ZS

    #
    # The "ALL_DEFINED_TABS" matrix is the only place where tabs should be defined.
    #
    ALL_DEFINED_TABS = [
        [NewRO,  NewRO,  'List',      'rlist'],
        [NewRW,  NewRW,  'Edit',      'wlist'],
        [UserRO, Admin,  'Directory', 'dlist'],
        [UserRO, Admin,  'Info',      'imenu'],
        [UserRW, UserRW, 'Edit',      'delst'],
        [Admin,  Admin,  'Admin',     'amenu'],
        ]

    for tab in ALL_DEFINED_TABS:
        if ZS['Authority'] >= tab[0] and ZS['Authority'] <= tab[1]:
            ZS['Tab'][tab[2]] = len(ZS['Tabs'])
            ZS['Tabs'] += [tab]

    try:
        if active_tab == '.':
            ZS['ActiveTab'] = 0
        else:
            ZS['ActiveTab'] = ZS['Tab'][active_tab]

        if ZS['Authority'] < ZS['Tabs'][ZS['ActiveTab']][0] or ZS['Authority'] > ZS['Tabs'][ZS['ActiveTab']][1]:
            ZS['ErrorMessage'] = '[WW03]: Invalid URL.'
    except:
        ZS['ErrorMessage'] = '[WW04]: URL contained an invalid destination.'

    return ZS
