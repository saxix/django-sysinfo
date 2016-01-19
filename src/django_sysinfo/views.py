# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import codecs
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .api import UNKNOWN, get_sysinfo, get_version
from .compat import JsonResponse

HTTP_HEADER_ENCODING = 'iso-8859-1'


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
                if user:
                    login(request, user)
                else:
                    raise PermissionDenied()
        return func(request, *args, **kwargs)

    return _decorator


def http_basic_login(func):
    return http_basic_auth(login_required(func))


# @http_basic_login
def sysinfo(request):
    return JsonResponse(get_sysinfo(request))


def version(request, name):
    version = get_version(name)
    if version == UNKNOWN:
        status = 404
    else:
        status = 200
    data = {name: version}
    return JsonResponse(data, status=status)
