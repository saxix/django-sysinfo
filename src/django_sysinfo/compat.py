# -*- coding: utf-8 -*-
import pkg_resources

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

stdlib_pkgs = ('python', 'wsgiref')


def get_installed_distributions(skip=stdlib_pkgs):
    """
    Return a list of installed Distribution objects.
    ``skip`` argument is an iterable of lower-case project names to
    ignore; defaults to stdlib_pkgs

    """
    return [d for d in pkg_resources.working_set
            if d.key not in skip]
