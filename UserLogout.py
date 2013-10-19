# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

import SessionSettings as Z
from UserLogin import GoLogout

def do(request):
    ZS = Z.SetWhoZwho(request, '')
    return GoLogout(request, ZS, '[UO01]: You have successfully logged out.')
