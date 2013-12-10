# Copyright (C) 2012 C. R. Leavett-Brown
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^amenu$',                                                       'WhoZwho.AdminMenu.do'),
    url(r'^alist$',                                                       'WhoZwho.AdminApprovalList.do'),
    url(r'^apprv/(?P<nid>\d+)$',                                          'WhoZwho.AdminApproveRemove.do'),
    url(r'^aelst$',                                                       'WhoZwho.AdminEditList.do'),
    url(r'^rilst$',                                                       'WhoZwho.AdminReinstateList.do'),
    url(r'^rinam/(?P<nid>\d+)$',                                          'WhoZwho.AdminRemoveReinstate.do'),
    url(r'^rmnam/(?P<nid>\d+)$',                                          'WhoZwho.AdminRemoveReinstate.dorm'),

    url(r'^delst',                                                        'WhoZwho.DirectoryEditList.do'),
    url(r'^ename/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',               'WhoZwho.DirectoryEditName.do'),
    url(r'^dlist$',                                                       'WhoZwho.DirectoryList.do'),
    url(r'^cfa/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',                 'WhoZwho.DirectoryAddresses.CreateFamily'),
    url(r'^efa/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',                 'WhoZwho.DirectoryAddresses.EditFamily'),
    url(r'^sfa/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',                 'WhoZwho.DirectoryAddresses.FamilyMenu'),
    url(r'^cia/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',                 'WhoZwho.DirectoryAddresses.CreateIndividual'),
    url(r'^eia/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',                 'WhoZwho.DirectoryAddresses.EditIndividual'),
    url(r'^sia/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',                 'WhoZwho.DirectoryAddresses.IndividualMenu'),
    url(r'^map/(?P<aid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',                 'WhoZwho.DirectoryAddresses.Map'),
    url(r'^sname/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',               'WhoZwho.DirectoryShowName.do'),
    url(r'^nname/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',               'WhoZwho.DirectoryAddName.do'),
    url(r'^married/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',             'WhoZwho.DirectoryDescribeFamily.married'),
    url(r'^singleparent/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',        'WhoZwho.DirectoryDescribeFamily.singleparent'),
    url(r'^individual/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',          'WhoZwho.DirectoryDescribeFamily.individual'),
    url(r'^nofamily/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',            'WhoZwho.DirectoryDeleteFamily.nofamily'),
    url(r'^rmpic/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',               'WhoZwho.DirectoryDeletePicture.do'),
    url(r'^print/(?P<option>[a-zA-Z]+)/(?P<browser_tab>[a-zA-Z]+)$',      'WhoZwho.DirectoryPrint.do'),

    url(r'^addpc/(?P<browser_tab>[a-zA-Z]+)$',                            'WhoZwho.DirectoryAddPrivateContact.do'),
    url(r'^purge/(?P<nid>\d+)/(?P<browser_tab>[a-zA-Z]+)$',               'WhoZwho.DirectoryDeleteByName.do'),

    url(r'^imenu$',                                                       'WhoZwho.InfoMenu.do'),
    url(r'^anlst$',                                                       'WhoZwho.InfoAnniversaries.do'),
    url(r'^stats$',                                                       'WhoZwho.InfoLoginStats.do'),

    url(r'^rlist$',                                                       'WhoZwho.NewROList.do'),
    url(r'^wlist$',                                                       'WhoZwho.NewRWList.do'),

    url(r'^login/$',                                                      'WhoZwho.UserLogin.do'),
    url(r'^logout/$',                                                     'WhoZwho.UserLogout.do'),
    url(r'^fgpwd$',                                                       'WhoZwho.UserForgotPassword.do'),
    url(r'^fglog$',                                                       'WhoZwho.UserForgotLogin.do'),
    url(r'^chpwd/(?P<browser_tab>[a-zA-Z]+)$',                            'WhoZwho.UserChangePassword.do'),
    url(r'^registration/$',                                               'WhoZwho.UserRegistration.now'),
)
