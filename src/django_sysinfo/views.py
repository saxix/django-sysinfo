# -*- coding: utf-8 -*-
import codecs
import logging
from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import never_cache

from django_sysinfo.conf import config

from .api import UNKNOWN, get_sysinfo, get_version, run_check

HTTP_HEADER_ENCODING = "iso-8859-1"

logger = logging.getLogger(__name__)


def is_authorized(user):
    if user.is_superuser:
        return True
    return user.username in getattr(settings, "SYSINFO_USERS", [])


def http_basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login
        if "HTTP_AUTHORIZATION" in request.META:
            authmeth, auth = request.META["HTTP_AUTHORIZATION"].split(" ", 1)
            if authmeth.lower() == "basic":
                auth = codecs.decode(auth.encode("utf8").strip(), "base64").decode()
                username, password = auth.split(":", 1)
                user = authenticate(username=username, password=password)
                if user and is_authorized(user):
                    login(request, user)
                else:
                    raise PermissionDenied()
        return func(request, *args, **kwargs)

    return _decorator


def http_basic_login(func):
    return http_basic_auth(login_required(func))


def sysinfo(request):
    KEY = 'sysinfo/info2'
    try:
        content = cache.get(KEY)

        if not content:
            content = get_sysinfo(request)

        if config.ttl > 0:
            cache.set(KEY, dict(content), config.ttl)

        response = JsonResponse(content, safe=False)
        patch_cache_control(response, max_age=config.ttl, public=False)

        return response
    except Exception as e:  # pragma: no cover
        logger.exception(e)
        return JsonResponse({"Error": str(e)}, status=400)


def version(request, name):
    version = get_version(name)
    if version == UNKNOWN:
        status = 404
    else:
        status = 200
    data = {name: version}
    return JsonResponse(data, status=status)


@never_cache
def echo(request, value):
    return HttpResponse(value)


def check(request, id):
    try:
        ret, status = run_check(id)
        return JsonResponse({"message": ret}, status=status)
    except Exception as e:  # pragma: no cover
        return JsonResponse({"error": str(e)}, status=500)


@user_passes_test(is_authorized)
def admin_sysinfo(request):
    infos = get_sysinfo(request)
    infos.setdefault('extra', {})
    infos.setdefault('checks', {})
    context = {'title': 'sysinfo',
               'infos': infos
               }
    return render(request, 'admin/sysinfo/sysinfo.html', context)
