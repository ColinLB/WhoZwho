# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

from django.db.models import Q
from models import Name
import string
import random

def GenerateTemporaryPassword(size=7, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def GetIndexedDirectoryNameLists(ZS):
    names = Name.objects.all(). \
        exclude(Q(private__exact=True) & ~Q(owner__exact=ZS['AuthorizedOwner'])). \
        exclude(removed__exact=True). \
        exclude(approved__exact=False). \
        exclude(first__isnull=True). \
        exclude(first__exact=''). \
        order_by('first', 'last')

    ix = 0
    iy = 1
    first_initials = []
    first_names = {}
    if len(names) > 0:
        for iy in range(1, len(names)):
            if names[iy].first[0] != names[ix].first[0]:
                if names[ix].first[0] not in first_initials:
                    first_initials += [names[ix].first[0]]
                first_names[names[ix].first[0]] = names[ix: iy]
                ix = iy

        if names[ix].first[0] not in first_initials:
            first_initials += [names[ix].first[0]]
        first_names[names[ix].first[0]] = names[ix: iy + 1]

    names = Name.objects.all(). \
        exclude(Q(private__exact=True) & ~Q(owner__exact=ZS['AuthorizedOwner'])). \
        exclude(removed__exact=True). \
        exclude(approved__exact=False). \
        exclude(last__isnull=True). \
        exclude(last__exact=''). \
        order_by('last', 'first')

    ix = 0
    iy = 1
    last_initials = []
    last_names = {}
    if len(names) > 0:
        for iy in range(1, len(names)):
            if names[iy].last[0] != names[ix].last[0]:
                if names[ix].last[0] not in last_initials:
                    last_initials += [names[ix].last[0]]
                last_names[names[ix].last[0]] = names[ix: iy]
                ix = iy

        if names[ix].last[0] not in last_initials:
            last_initials += [names[ix].last[0]]
        last_names[names[ix].last[0]] = names[ix: iy + 1]

    return [ first_initials, first_names, last_initials, last_names ]

def SaveFileUpload(infile, outfile):
    destination = open(outfile, 'wb+')
    for chunk in infile.chunks():
        destination.write(chunk)
    destination.close()
