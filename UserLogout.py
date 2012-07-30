# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import WhoZwho as Z
from UserLogin import GoLogout

def do(request):
    WZ = Z.SetWhoZwho(request, '')
    return GoLogout(request, WZ, '[UO01]: You have successfully logged out.')
