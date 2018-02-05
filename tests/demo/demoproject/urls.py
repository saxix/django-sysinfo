from __future__ import absolute_import

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.signals import request_started
from django.db import IntegrityError
from django.dispatch import receiver

from django_sysinfo.views import (
    admin_sysinfo, check, echo, http_basic_login, sysinfo, version
)

urlpatterns = (
    url("sys/info-auth/$", http_basic_login(sysinfo), name="sys-info-auth"),
    # url(r"", include('django_sysinfo.urls')),

    url("sys/info/$", sysinfo, name="sys-info"),
    url("sys/version/(?P<name>.*)/$", version, name="sys-version"),
    url("sys/echo/(?P<value>.*)/$", echo, name="sys-echo"),
    url("check/(?P<id>.*)/$", check, name="sys-check"),
    url("admin/sysinfo/$", admin_sysinfo, name="sys-admin-info"),

    # url("info/$", http_basic_login(sysinfo), name="sys-info"),
    # url("version/(?P<name>.*)/$", http_basic_login(version), name="sys-version"),
    # url("echo/(?P<value>.*)/$", echo, name="sys-echo"),
    # url("check/(?P<id>.*)/$", http_basic_login(check), name="sys-check"),

    url(r"admin/", admin.site.urls),
)


@receiver(request_started)
def c(*args, **kwargs):
    try:
        user = User(username="sax", email="")
        user.set_password("123")
        user.set_password("123")
        user.save()
    except IntegrityError:
        pass
