# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.apps import apps

from django_sysinfo.utils import get_package_version


def get_installed_apps():
    installed_apps = []
    for app_config in apps.get_app_configs():
        installed_apps.append([app_config.name,
                               get_package_version(app_config.name, app_config.module)])
    return sorted(installed_apps)


try:
    from django.urls import reverse  # noqa
except ImportError:
    from django.core.urlresolvers import reverse  # noqa
