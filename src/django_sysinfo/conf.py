# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings


def merge(a, b, path=None):
    """merges b into a

    >>> a={1:{"a":"A"},2:{"b":"B"}, 8:[]}
    >>> b={2:{"c":"C"},3:{"d":"D"}}

    >>> c = merge(a, b)
    >>> c == a == {8: [], 1: {"a": "A"}, 2: {"c": "C", "b": "B"}, 3: {"d": "D"}}
    True

    >>> c = merge(a, {1: "a"})
    >>> print(c[1])
    a
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
                # raise Exception("Conflict at %s (%s %s)" % (".".join(path + [str(key)]),
                #                 a[key], b[key]))
        else:
            a[key] = b[key]
    return a


DEFAULTS = {"os": False,
            "modules": False,
            "python": False,
            "host": False,
            "extra": False,
            "checks": {},
            "project": {
                "mail": False,
                "databases": False,
                "MEDIA_ROOT": False,
                "STATIC_ROOT": False,
                "CACHES": False}
            }


class Config(object):
    """
    >>> c = Config({"os": True})
    >>> c.os, c.python
    (True, False)
    >>> c = Config({"os": True, "project": False})
    >>> c.project
    False

    """

    def __init__(self, config):
        self._config = DEFAULTS.copy()
        merge(self._config, config)

    def __getattr__(self, item):
        if item in self._config:
            return self._config[item]
        elif item in self._config["project"]:
            if not self._config["project"]:
                return False
            return self._config["project"][item]
        raise AttributeError

    def __repr__(self):
        return str({"host": self.host,
                    "os": self.os,
                    "mail": self.mail,
                    "python": self.python,
                    "modules": self.modules,
                    "project": self.project,
                    "databases": self.databases,
                    "installed_apps": self.installed_apps,
                    "extra": self.extra
                    })


config = Config(getattr(settings, "SYSINFO", {}))
