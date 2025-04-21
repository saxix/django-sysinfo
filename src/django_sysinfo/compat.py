from operator import itemgetter

from django.apps import apps

from django_sysinfo.utils import get_package_version


def get_installed_apps():
    installed_apps = [
        (app_config.name, get_package_version(app_config.name, app_config.module))
        for app_config in apps.get_app_configs()
    ]
    return sorted(installed_apps, key=itemgetter(0))


try:
    from django.urls import reverse  # noqa
except ImportError:
    from django.core.urlresolvers import reverse  # noqa

stdlib_pkgs = ("python", "wsgiref")
