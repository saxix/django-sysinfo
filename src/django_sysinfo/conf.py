# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings


class Config(object):
    def __init__(self):
        SYSINFO = getattr(settings, 'SYSINFO', {})
        self.databases = SYSINFO.get('databases', True)
        self.django = SYSINFO.get('django', True)
        self.modules = SYSINFO.get('modules', True)
        self.installed_apps = SYSINFO.get('installed_apps', True)
        self.host = SYSINFO.get('host', True)
        self.project = SYSINFO.get('project', True)
        self.python = SYSINFO.get('python', True)
        self.os = SYSINFO.get('os', True)
        self.extra = SYSINFO.get('extra', None)


config = Config()
