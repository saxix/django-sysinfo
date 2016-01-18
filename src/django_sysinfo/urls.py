# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from django_sysinfo.views import sysinfo, version

urlpatterns = (
    url('sys/info/$', sysinfo, name='sys-info'),
    url('sys/version/(?P<name>.*)/$', version, name='sys-version')
)
