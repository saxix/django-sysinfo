# -*- coding: utf-8 -*-
from django.urls import path

from django_sysinfo.views import check, echo, sysinfo, version

urlpatterns = (
    path("sys/info/$", sysinfo, name="sys-info"),
    path("sys/version/<str:name>/$", version, name="sys-version"),
    path("sys/echo/<str:value>/$", echo, name="sys-echo"),
    path("check/<str:id>/$", check, name="sys-check"),
)
