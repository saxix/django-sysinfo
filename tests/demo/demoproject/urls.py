from __future__ import absolute_import

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.signals import request_started
from django.db import IntegrityError
from django.dispatch import receiver

import django_sysinfo.urls
from django_sysinfo.views import http_basic_login, sysinfo

urlpatterns = (
    url("sys/info-auth/$", http_basic_login(sysinfo), name="sys-info-auth"),
    url(r"", include(django_sysinfo.urls)),
    url(r"admin/", include(admin.site.urls)),
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
