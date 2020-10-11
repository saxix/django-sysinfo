# -*- coding: utf-8 -*-
from django.conf.urls import url

from django_sysinfo.views import check, echo, http_basic_login, sysinfo, version

urlpatterns = (
    url("info/$", http_basic_login(sysinfo), name="sys-info"),
    url("version/(?P<name>.*)/$", http_basic_login(version), name="sys-version"),
    url("echo/(?P<value>.*)/$", echo, name="sys-echo"),
    url("check/(?P<id>.*)/$", http_basic_login(check), name="sys-check"),
)
