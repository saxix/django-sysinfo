# -*- coding: utf-8 -*-
# flake8:noqa
from __future__ import absolute_import, print_function, unicode_literals

import logging
from pkg_resources import get_distribution

import django

logger = logging.getLogger(__name__)

if django.VERSION[:2] == (1, 6):
    def get_istalled_apps():
        installed_apps = []
        from django.conf import settings

        for app_name in settings.INSTALLED_APPS:
            try:
                mod = __import__(app_name)
                installed_apps.append([app_name,
                                       get_distribution(mod.__name__).version])
            except:
                pass
        return installed_apps

    from django.http import HttpResponse
    from django.core.serializers.json import DjangoJSONEncoder
    import json


    class JsonResponse(HttpResponse):
        def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
            kwargs.setdefault('content_type', 'application/json')
            data = json.dumps(data, cls=encoder)
            super(JsonResponse, self).__init__(content=data, **kwargs)

elif django.VERSION[1] in [7, 8, 9, 10]:
    from django.apps import apps
    from django.http import JsonResponse, HttpResponse


    def get_istalled_apps():
        installed_apps = []
        for app_config in apps.get_app_configs():
            try:
                installed_apps.append([app_config.name,
                                       get_distribution(app_config.name).version])
            except:
                pass
        return installed_apps

else:
    raise EnvironmentError('Django version not supported')
