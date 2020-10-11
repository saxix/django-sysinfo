# -*- coding: utf-8 -*-
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


DEFAULTS = {"_ttl": 0,
            "filter_environment": "django_sysinfo.utils.filter_env",
            "masked_environment": ["PASS", "SECRET", "PASSWORD", "KEY"],
            "hidden_environment": [],
            "os": True,
            "modules": True,
            "python": True,
            "host": True,
            "extra": {},
            "checks": {},
            "installed_apps": True,
            "environ": True,
            "project": {
                "mail": True,
                "databases": True,
                "MEDIA_ROOT": True,
                "STATIC_ROOT": True,
                "CACHES": True}
            }


class Config(object):
    """
    >>> c = Config({"os": False})
    >>> c.os, c.python, c.project['mail'], c.MEDIA_ROOT
    (False, True, True, True)
    >>> c = Config({"os": True, "installed_apps": False})
    >>> c.installed_apps
    False
    >>> assert repr(c)
    """

    def __init__(self, config):
        self._config = DEFAULTS.copy()
        merge(self._config, config)

    @property
    def ttl(self):
        return int(self._ttl)

    def __getattr__(self, item):
        if item in self._config:
            return self._config[item]
        elif item in self._config["project"]:
            # if not self._config["project"]:
            #     return False
            return self._config["project"][item]
        return None
        # raise AttributeError("Config does not have attribute {}".format(item))

    def __repr__(self):
        return str({"host": self.host,
                    "os": self.os,
                    "mail": self.mail,
                    "python": self.python,
                    "modules": self.modules,
                    "environ": self.environ,
                    "project": self.project,
                    "databases": self.databases,
                    "installed_apps": self.installed_apps,
                    "extra": self.extra
                    })


config = Config(getattr(settings, "SYSINFO", {}))
