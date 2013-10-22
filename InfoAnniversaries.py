# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import os.path
from django.http import HttpResponse
from django.template import Context, loader
from django.db.models import Q
from models import Address, Name, Wedding

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def do(request):
    ZS = Z.SetSession(request, 'Info')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    list = []
    weddings = Wedding.objects.all()
    for wedding in weddings:
        names = wedding.name_set.all(). \
            exclude(private__exact=True)
        if len(names) != 2:
            continue

        if names[0].removed == True or names[0].approved == False:
            continue

        if names[1].removed == True or names[1].approved == False:
            continue

        if wedding.anniversary:
            if names[0].gender == 'm':
                list += [ FormatAnniversary(wedding.anniversary, names[0], names[1]) ]
            else:
                list += [ FormatAnniversary(wedding.anniversary, names[1], names[0]) ]

    [ anniversaries, anniversary_months] = MakeDictionary(list)

    list = []
    names = Name.objects.all(). \
        exclude(private__exact=True). \
        exclude(removed__exact=True). \
        exclude(approved__exact=False)

    for name in names:
        if name.birthday:
            list += [ FormatAnniversary(name.birthday, name, None) ]

    [ birthdays, birthday_months] = MakeDictionary(list)

    months = []
    for month in sorted(anniversary_months + birthday_months, key=lambda mm: mm[0]):
        if not month[1] in months:
            months += [ month[1] ]


#    print str(months)
#    print str(days)

#    if request.COOKIES.has_key('dlist_parm'):
#        dlist_parm = request.COOKIES['dlist_parm']
#    else:
#        dlist_parm = 'F..'

    template = loader.get_template('InfoAnniversaries.html')
    context = Context({
        'months': months,
        'birthdays': birthdays,
        'anniversaries': anniversaries,
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
    return response

def FormatAnniversary(d, n1, n2):
    if n2 == None:
        n = n1.first + ' ' + n1.last
    else:
        if n2.last == n1.last:
            n = n1.first + ' & ' + n2.first + ' ' + n1.last
        else:
            n = n1.first + ' ' + n1.last + ' & ' + n2.first + " " + n2.last

    return (
        '%02d' % d.month + '%02d' % d.day,
        Z.Months[d.month - 1],
        '%02d' % d.day,
        n,
        )

def MakeDictionary(list):
    # List contains: [ mmdd, month, dd, name(s) ]
    sorted_list = sorted(list, key=lambda mmdd: mmdd[0])

    months = []
    days = {}
    for day in sorted_list:
        months += [ [ day[0][0:2], day[1] ] ]

        if not days.has_key(day[1]):
            days[day[1]] = []

        days[day[1]] += [ day[2] + ' ' + day[3] ]

    return [ days, months ]
