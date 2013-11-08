# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

from django.db.models import Q
from models import Name
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

def SaveFileUpload(infile, outfile):
    destination = open(outfile, 'wb+')
    for chunk in infile.chunks():
        destination.write(chunk)
    destination.close()
