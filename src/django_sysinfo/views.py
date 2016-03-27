# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import codecs
from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from .api import UNKNOWN, get_sysinfo, get_version
from .compat import JsonResponse

HTTP_HEADER_ENCODING = 'iso-8859-1'


def is_authorized(user):
    if user.is_superuser:
        return True
    return user.username in getattr(settings, 'SYSINFO_USERS', [])


def http_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login

        if 'HTTP_AUTHORIZATION' in request.META:
            authmeth, auth = request.META['HTTP_AUTHORIZATION'].split(b' ', 1)
            if authmeth.lower() == b'basic':
                auth = codecs.decode(auth.strip(), 'base64')
                username, password = auth.split(b':', 1)
                user = authenticate(username=username, password=password)
                if user and is_authorized(user):
                    login(request, user)
                else:
                    raise PermissionDenied()
        return func(request, *args, **kwargs)

    return _decorator


def http_basic_login(func):
    return http_basic_auth(login_required(func))


# @http_basic_login
def sysinfo(request):
    try:
        return JsonResponse(get_sysinfo(request))
    except Exception as e:
        return JsonResponse({'Error': str(e)}, status=400)


def version(request, name):
    version = get_version(name)
    if version == UNKNOWN:
        status = 404
    else:
        status = 200
    data = {name: version}
    return JsonResponse(data, status=status)


def echo(request, value):
    return HttpResponse(value)
