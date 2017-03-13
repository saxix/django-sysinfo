# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings


class Config(object):
    def __init__(self):
        SYSINFO = getattr(settings, "SYSINFO", {})
        self.databases = SYSINFO.get("databases", False)
        self.modules = SYSINFO.get("modules", False)
        # self.installed_apps = SYSINFO.get("installed_apps", False)
        self.host = SYSINFO.get("host", False)
        self.project = SYSINFO.get("project", False)
        self.installed_apps = SYSINFO.get("project.installed_apps", False)
        self.MEDIA_ROOT = SYSINFO.get("project.MEDIA_ROOT", False)
        self.STATIC_ROOT = SYSINFO.get("project.STATIC_ROOT", False)
        self.CACHES = SYSINFO.get("project.CACHES", False)
        self.python = SYSINFO.get("python", False)
        self.os = SYSINFO.get("os", False)
        self.extra = SYSINFO.get("extra", False)

    def __repr__(self):
        return str({"host": self.host,
                    "os": self.os,
                    "python": self.python,
                    "modules": self.modules,
                    "project": self.project,
                    "databases": self.databases,
                    "installed_apps": self.installed_apps,
                    "extra": self.extra
                    })


config = Config()
