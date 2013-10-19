# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

from subprocess import PIPE, Popen, STDOUT
from django.http import HttpResponse
from django.template import Context, loader
from models import Name

def do(request):
    ZS = Z.SetWhoZwho(request, 'Info')
    if ZS['ErrorMessage']:
        return GoLogout(request, ZS, '')

#	'/var/log/WhoZwho-update.log',
#	'/var/log/django/WhoZwho.log',

    p = Popen(['awk',
	'/logged in/ {if (x[$4]=="") {x[$4]=0} x[$4]+=1} END{for(y in x) printf "%-24s = %d\\n", y, x[y]}',
    ZS['UpdateLogFN'],
	], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

    stats = stdout.splitlines()

    template = loader.get_template('InfoLoginStats.html')
    context = Context({
        'stats': sorted(stats),
        'ZS': ZS,
        })

    return HttpResponse(template.render(context))
