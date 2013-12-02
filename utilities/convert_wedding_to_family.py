# Make sure our parent directory cantains a symlink to the project directory, eg. ln -s /home/whozwho/django/my_site
# and export DJANGO_SETTINGS_MODULE='my_site.settings'
import sys
sys.path.append("esquimalt")

from WhoZwho.models import Family, Name, Wedding

print 'Families:'
families = Family.objects.all()
for family in families:
    print str(family.id) + " " + str(family.owner) + " " + str(family.anniversary) + " " + str(family.spouses.all()[0].first) + " " + str(family.spouses.all()[1].first) + " " + str(family.email)

print 'Weddings:'
weddings = Wedding.objects.all()
for wedding in weddings:
    print str(wedding.id) + " " + str(wedding.owner) + " " + str(wedding.anniversary) + " " + wedding.name_set.all()[0].first + " " + wedding.name_set.all()[1].first + " " + wedding.email

#   family = Family()
#   family.owner = wedding.owner

#   if wedding.anniversary:
#       family.anniversary = wedding.anniversary

#   if wedding.email:
#       family.email = wedding.email

#   family.save()

#   names = wedding.name_set.all()
#   for name in names:
#        name.family = family
#        name.save()

