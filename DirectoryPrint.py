# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

import os.path
from django.http import HttpResponse
from django.template import Context, loader
from django.db.models import Q
from models import Address, Name, Wedding

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def do(request, browser_tab):
    WZ = Z.SetWhoZwho(request, browser_tab)
    if WZ['ErrorMessage']:
        return GoLogout(request, WZ, '')

    list = []
    weddings = Wedding.objects.all()
    for wedding in weddings:
        names = wedding.name_set.all(). \
            exclude(Q(private__exact=True) & ~Q(owner__exact=WZ['AuthorizedOwner']))
        if len(names) != 2:
            continue

        if names[0].removed == True or names[0].approved == False:
            continue

        if names[1].removed == True or names[1].approved == False:
            continue

        list += [ FormatName(WZ, names[0], names[1]) + FormatAddress(names[0].address) ]

    names = Name.objects.all(). \
        filter(wedding__exact=None). \
        exclude(Q(private__exact=True) & ~Q(owner__exact=WZ['AuthorizedOwner'])). \
        exclude(removed__exact=True). \
        exclude(approved__exact=False)

    for name in names:
        list += [ FormatName(WZ, name, None) + FormatAddress(name.address) ]

    for item in sorted(list):
        print str(item)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=WhoZwho.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica", 24)


    p.drawString(60, 500, WZ['Banner'])

    row = 0
    page = 0
    pages = str((len(list) + 4) / 5)
    for item in sorted(list):
        if row < 50:
            p.showPage()
            page += 1
            row = 610

            p.setFont("Helvetica", 10)
            p.drawString(300, 10, str(page) + '/' + pages)

        p.drawImage(item[1], 60, row, width=100,height=125,mask=None)

        if item[2] != '':
            p.drawImage(item[2], 185, row, width=100,height=125,mask=None)

        p.setFont("Helvetica", 16)
        p.drawString(310, row + 115, item[0])

        p.setFont("Helvetica", 12)
        p.drawString(310, row + 100, item[6])
        p.drawString(310, row +  85, item[7])
        p.drawString(310, row +  70, item[8])
        
        p.drawString(310, row +  50, item[9])

        p.drawString(310, row +  30, item[3])
        p.drawString(310, row +  15, item[4])
        p.drawString(310, row +  00, item[5])

        row -= 140

    p.showPage()
    p.save()

    return response

def FormatAddress(addr):
    if addr:
        formatted_address = [addr.street, addr.city, addr.province + ', ' + addr.postcode, addr.phone]
    else:
        formatted_address = ['', '', '', '']

    return formatted_address

def FormatName(WZ, n1, n2):
    m = []

    if n2:
        n = n1.last + ', ' + n1.first + ' & ' + n2.first
        if os.path.exists(WZ['StaticPath'] + 'pics/names/' + str(n2.id) + '.jpg'):
            p2 = WZ['StaticPath'] + 'pics/names/' + str(n2.id) + '.jpg'
        else:
            p2 = WZ['StaticPath'] + 'pics/names/default.jpg'

        if n1.wedding.email:
            m += [ n1.wedding.email + "  (joint)" ]

        if n1.email:
            m += [ n1.email + "  (" + n1.first + ")" ]

        if n2.email:
            m += [ n2.email + "  (" + n2.first + ")" ]

    else:
        p2 = ''
        n = n1.last + ', ' + n1.first
        m += [ n1.email ]

    if os.path.exists(WZ['StaticPath'] + 'pics/names/' + str(n1.id) + '.jpg'):
        p1 = WZ['StaticPath'] + 'pics/names/' + str(n1.id) + '.jpg'
    else:
        p1 = WZ['StaticPath'] + 'pics/names/default.jpg'

    while len(m) < 3:
        m += [ '' ]

    return [ n, p1, p2, m[0], m[1], m[2]]

