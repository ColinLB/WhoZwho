# Make sure our parent directory contains a symlink to the project directory, eg. ln -s /home/my_id/django/my_site
# and export DJANGO_SETTINGS_MODULE='my_site.settings'
import sys
sys.path.append("esquimalt")

from WhoZwho.models import Address, Family, Name

print 'Families:'
families = Family.objects.all()
for family in families:
    spouses = family.spouses.all()
    if len(spouses) > 1:
        print str(family.id) + " " + str(family.spouses.all()[0].first) + " " + str(family.spouses.all()[1].first)
    else:
        print str(family.id) + " " + str(family.spouses.all()[0].first) 

    if not family.address:
        if spouses[0].address:
            family.address = spouses[0].address
            family.save()
        elif len(spouses) > 1 and spouses[1].address:
            family.address = spouses[1].address
            family.save()

    if spouses[0].address and spouses[0].address == family.address:
        spouses[0].address = None
        spouses[0].save()

    if len(spouses) > 1:
        if spouses[1].address and spouses[1].address == family.address:
            spouses[1].address = None
            spouses[1].save()
