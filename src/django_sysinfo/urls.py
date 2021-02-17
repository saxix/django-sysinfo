# -*- coding: utf-8 -*-
from django.urls import path

from django_sysinfo.views import check, echo, http_basic_login, sysinfo, version

urlpatterns = (
    path("info/$", http_basic_login(sysinfo), name="sys-info"),
    path("version/<str:name>/$", http_basic_login(version), name="sys-version"),
    path("echo/<str:value>/$", echo, name="sys-echo"),
    path("check/<str:id>/$", http_basic_login(check), name="sys-check"),
)
