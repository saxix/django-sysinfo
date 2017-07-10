# -*- coding: utf-8 -*-
# flake8:noqa
from __future__ import absolute_import, print_function, unicode_literals

import logging
from pkg_resources import get_distribution

import django

logger = logging.getLogger(__name__)

if django.VERSION[1] in [7, 8, 9, 10, 11]:
    from django.apps import apps

    def get_installed_apps():
        installed_apps = []
        for app_config in apps.get_app_configs():
            try:
                installed_apps.append([app_config.name,
                                       get_distribution(app_config.name).version])
            except:
                pass
        return installed_apps

else:  # pragma: no cover
    raise EnvironmentError('Django version not supported')
