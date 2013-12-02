# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

import os.path
from django.http import HttpResponse
from django.template import Context, loader
from django.db.models import Q
from models import Address, Family, Name, Wedding

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from SessionFunctions import Age, FamilyAddress, FamilyName, Kids, NameContacts


def do(request, option, browser_tab):
    ZS = Z.SetSession(request, browser_tab)
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

    # Retrieve information for family entries.
    listC, listCA, listCM, listF, listFA, listFM = [], [], [], [], [], []
    families = Family.objects.all()
    for family in families:
        spouses = family.spouses.all(). \
            exclude(approved__exact=False). \
            exclude(Q(private__exact=True) & ~Q(owner__exact=ZS['AuthorizedOwner'])). \
            exclude(removed__exact=True)
        if len(spouses) < 1:
            continue

        attends_church = False
        if spouses[0].out_of_town == False:
            attends_church = True
        elif len(spouses) == 2 and spouses[1].out_of_town == False:
            attends_church = True

        if family.anniversary:
            family_anniversary = SortableMonth(family.anniversary) + ['a', FamilyName(spouses[0], 'firstlast')]
            if attends_church:
                listCA += [ family_anniversary ]
            else:
                listFA += [ family_anniversary ]

        if len(spouses) < 2:
            contacts = PersonalContacts(spouses[0])
        else:
            if spouses[0].gender == 'm':
                contacts  = PersonalContacts(spouses[0])
                contacts += PersonalContacts(spouses[1]) 
            else:
                contacts  = PersonalContacts(spouses[1])
                contacts += PersonalContacts(spouses[0]) 

        children = family.children.all(). \
            exclude(approved__exact=False). \
            exclude(Q(private__exact=True) & ~Q(owner__exact=ZS['AuthorizedOwner'])). \
            exclude(removed__exact=True)

        for child in children:
            contacts += PersonalContacts(child)

        if family.picture_uploaded:
            directory_entry = [ 'pics/families/' + str(family.id) + '.jpg', [ FamilyName(spouses[0]), Kids(spouses[0], '  ') ] + FamilyAddress(spouses[0], '    ') + [u''] + contacts ]
        else:
            directory_entry = [ 'pics/defaults/nicubunu_Abstract_people.png', [ FamilyName(spouses[0]), Kids(spouses[0], '  ') ] + FamilyAddress(spouses[0], '    ') + [u''] + contacts ]
        if attends_church:
            listC += [ directory_entry ]
        else:
            listF += [ directory_entry ]

    # Retrieve information for individual entries.
    names = Name.objects.all(). \
        exclude(approved__exact=False). \
        exclude(Q(private__exact=True) & ~Q(owner__exact=ZS['AuthorizedOwner'])). \
        exclude(removed__exact=True)

    for name in names:
        if name.birthday:
            birthday = SortableMonth(name.birthday) + ['b', name.first + ' ' + name.last]
            if name.out_of_town == True:
                listFA += [ birthday ]
            else:
                listCA += [ birthday ]

        if name.family:
            continue

#       #member
#       if name.member:
#           directory_entry = [name.last + ', ' + name.first, str(name.member.year()) ]
#           if name.out_of_town == True:
#               listFM += [ directory_entry ]
#           else:
#               listCM += [ directory_entry ]

        if name.parents and Age(name.birthday) < 18:
            continue

        if name.picture_uploaded:
            directory_entry = [ 'pics/names/' + str(name.id) + '.jpg', [ FamilyName(name), '' ] + FamilyAddress(name, '    ') + [u''] + PersonalContacts(name) ]
        else:
            directory_entry = [ 'pics/defaults/nicubunu_Abstract_people.png', [ FamilyName(name), '' ] + FamilyAddress(name, '    ') + [u''] + PersonalContacts(name) ]

        if name.out_of_town == True:
            listF += [ directory_entry ]
        else:
            listC += [ directory_entry ]

    # Sorting and pagination.
    pages = []
    pages += Pagination('C', sorted(listC, key=lambda last_name: last_name[1]), 5)
    listC = None

    pages += Pagination('CA', sorted(listCA, key=lambda date: date[0]), 52)
    listCA = None

    pages += Pagination('F', sorted(listF, key=lambda last_name: last_name[1]), 5)
    listF = None

    pages += Pagination('FA', sorted(listFA, key=lambda date: date[0]), 52)
    listFA = None

    # Print report.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=WhoZwho.pdf'

    Canvas = canvas.Canvas(response, pagesize=landscape(letter))
    page_number, page_count = 0, len(pages)

    if option == "list":
        for page in pages:
            page_number += 1
            PrintPage(ZS, Canvas, page, page_number)

    else:
        padded_page_count = (page_count + 3) / 4 * 4
        for i in range(1, (padded_page_count / 2) + 1):
            j = 1 + padded_page_count - i
            try:
                PrintPage(ZS, Canvas, pages[j-1], j, padded_page_count)
            except:
                PrintPage(ZS, Canvas, [None], j, padded_page_count)
            PrintPage(ZS, Canvas, pages[i-1], i, padded_page_count)
        
    Canvas.save()
    return response

def FormatPage(ZS, canvas, page, page_number, Q):
    # Set page format as two pages, side by side on a landscape sheet.
    sheet_height, sheet_width, margin = 612, 792, 36
    page_height, page_width = sheet_height - (margin * 2), (sheet_width / 2) - (margin * 2)
    page_centre, page_title_offset, page_number_offset = page_width / 2, 590, 18
    if Q[1] == 'L':
        left_side = margin
    else:
        left_side = (sheet_width / 2) + margin

    # Draw page frame.
    canvas.setLineWidth(.3)
    canvas.rect(X(left_side-5,Q), Y(31,Q), 334, 550, stroke=1, fill=0) 
    canvas.setFont("Helvetica", 6)
    canvas.drawCentredString(X(left_side+162,Q), Y(page_number_offset,Q), '- ' + str(page_number) + ' -')

    if page[0] == None:
        return

    # Format a directory page:
    #
    #         Leavett-Brown, Colin & Glenda
    #           Holly
    #             2921 Merle Drive
    #             Victoria, BC, V9B 2H9
    #             crlb@telus.net, 250-478-7879
    #
    #         Colin: crlb@telus.net, 250-818-4560, work: crlb@uvic.ca, 250-472-4085
    #         Glenda: email, cell, work_email, work_phone
    #         Holly: email, cell, work_email, work_phone
    #
    if page[0] == 'C' or page[0] == 'F':
        cell_origin, cell_height = 470, 107
        canvas.setFont("Helvetica-Oblique", 14)
        if page[0] == 'C':
            canvas.drawCentredString(X(left_side+page_centre,Q), Y(page_title_offset,Q), ZS['Banner'])
        else:
            canvas.drawCentredString(X(left_side+page_centre,Q), Y(page_title_offset,Q), 'Family & Friends')

        canvas.line(X(left_side+90,Q), Y(31,Q), X(left_side+90,Q), Y(581,Q))
        canvas.line(X(left_side-5,Q), Y(467,Q), X(left_side+329,Q), Y(467,Q))
        canvas.line(X(left_side-5,Q), Y(360,Q), X(left_side+329,Q), Y(360,Q))
        canvas.line(X(left_side-5,Q), Y(253,Q), X(left_side+329,Q), Y(253,Q))
        canvas.line(X(left_side-5,Q), Y(146,Q), X(left_side+329,Q), Y(146,Q))

        for entry in page[1]:
            cell_offset = 90
            canvas.drawImage(ZS['StaticPath'] + entry[0], X(left_side,Q), Y(cell_origin,Q), width=80,height=100,mask=None)
            canvas.setFont("Helvetica", 10)
            for line in entry[1]:
                canvas.drawString(X(left_side+100,Q), Y(cell_origin+cell_offset,Q), line)
                cell_offset -= 10
            cell_origin -= cell_height

    # Format an anniversary page.
    #
    #                              April
    #
    #  7 Laurie & Katie Leavett-Brown  24 Lindsey Leavett-brown
    # 16 Holly Leavett-Brown
    #
    if page[0] == 'CA' or page[0] == 'FA':
        # Scan page content and divide into monthly sections.
        sections, start, end, month = [], 0, 0, ''
        for entry in page[1]:
            end += 1
            if month != entry[1]:
                if month != '':
                    sections += [ page[1][start:end-1] ]
                    start = end - 1

                month = entry[1]

        if end > start:
            sections += [ page[1][start:end] ]

        # Determine spacing.
        line_height, right_side = 9, page_width / 2
        page_offset = margin + page_height - line_height
        section_title_space = line_height * 2 * len(sections)
        section_data_space = line_height * ((len(page[1]) / 2) + ((len(sections) + 1) / 2))
        month_title_height, month_title_offset = line_height + 3, line_height / 2

        white_space = ((page_height - section_title_space - section_data_space) / line_height) - line_height
        if white_space < 0:
            white_space = 0
        elif white_space > line_height * 4:
            white_space = line_height * 4

        # Print title.
        canvas.setFont("Helvetica-Oblique", 14)
        if page[0] == 'CA':
            canvas.drawCentredString(X(left_side+page_centre,Q), Y(page_title_offset,Q), 'Church: Birthdays & Anniversaries*')
        else:
            canvas.drawCentredString(X(left_side+page_centre,Q), Y(page_title_offset,Q), 'Friends: Birthdays & Anniversaries*')

        # Print monthly sections.
        section = 0
        for month in sections:
            section += 1

            page_offset -= line_height
            canvas.setFont("Helvetica-Bold", month_title_height)
            canvas.drawCentredString(X(left_side+page_centre,Q), Y(page_offset+month_title_offset,Q), month[0][1])
            page_offset -= line_height

            entries = len(month)
            entry_offset = (entries + 1) / 2
            for entry in range(entry_offset):
                if month[entry][3] == 'b':
                    canvas.setFont("Helvetica", line_height)
                    pfx=''
                else:
                    canvas.setFont("Helvetica", line_height)
                    pfx='*'

                canvas.drawRightString(X(left_side+10,Q), Y(page_offset,Q), str(month[entry][2]))
                canvas.drawString(X(left_side+12,Q), Y(page_offset,Q), month[entry][4] + pfx)

                if entry+1 < entry_offset:
                    if month[entry+entry_offset][3] == 'b':
                        canvas.setFont("Helvetica", line_height)
                        pfx=''
                    else:
                        canvas.setFont("Helvetica", line_height)
                        pfx='*'

                    canvas.drawRightString(X(left_side+right_side+10,Q), Y(page_offset,Q), str(month[entry+entry_offset][2]))
                    canvas.drawString(X(left_side+right_side+12,Q), Y(page_offset,Q), month[entry+entry_offset][4] + pfx)

                page_offset -= line_height

            if section < len(sections):
                page_offset -= white_space
                canvas.line(X(left_side-5,Q), Y(page_offset,Q), X(left_side+329,Q), Y(page_offset,Q))
                page_offset -= line_height

def Pagination(tag, list, items_per_page):
    pages = []
    for i in range(0,len(list),items_per_page):
        pages += [ [tag, list[i:i+items_per_page]] ]

    return pages

def PersonalContacts(name):
    contacts = NameContacts(name)
    if contacts != '':
        return [ contacts ]
    else:
        return []

def PrintPage(ZS, canvas, page, page_number, page_count=0):
    if page_count > 0:
        if page_number <= (page_count / 2):
            if page_number % 2 == 1:
                FormatPage(ZS, canvas, page, page_number, 'TR')
                canvas.showPage()
            else:
                FormatPage(ZS, canvas, page, page_number, 'BL')
                canvas.showPage()
        else:
            if page_number % 2 == 0:
                FormatPage(ZS, canvas, page, page_number, 'TL')
            else:
                canvas.rotate(180)
                FormatPage(ZS, canvas, page, page_number, 'BR')
    else:
        if page_number % 2 == 1:
            FormatPage(ZS, canvas, page, page_number, 'TL')
        else:
            FormatPage(ZS, canvas, page, page_number, 'TR')
            canvas.showPage()

def SortableMonth(date):
    dd = date.day
    mm = date.month
    return ["%02d" % mm + "%02d" % dd, Z.Months[mm-1], str(dd)]

def X(coordinate, quadrant):
    if quadrant[0] == 'T':
        return coordinate
    else:
        return (792 - coordinate) * -1

def Y(coordinate, quadrant):
    if quadrant[0] == 'T':
        return coordinate
    else:
        return (618 - coordinate) * -1
