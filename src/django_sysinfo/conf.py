from django.conf import settings


def merge(a, b, path=None):
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


DEFAULTS = {
    "_ttl": 0,
    "filter_environment": "django_sysinfo.utils.filter_environment",
    "masked_environment": "API|TOKEN|KEY|SECRET|PASS|SIGNATURE|AUTH|_ID|SID",
    "masker": "django_sysinfo.utils.cleanse_setting",
    "hidden_environment": ["DIRENV_DIFF"],
    "os": True,
    "modules": True,
    "python": True,
    "host": True,
    "extra": {},
    "checks": {},
    "installed_apps": True,
    "process": True,
    "environ": True,
    "project": {"mail": True, "databases": True, "MEDIA_ROOT": True, "STATIC_ROOT": True, "CACHES": True},
}


class Config:
    def __init__(self, config):
        self._config = DEFAULTS.copy()
        merge(self._config, config)

    @property
    def ttl(self):
        return int(self._ttl)

    def __getattr__(self, item):
        if item in self._config:
            return self._config[item]
        if item in self._config["project"]:
            return self._config["project"][item]
        return None

    def __repr__(self):
        return str(
            {
                "host": self.host,
                "os": self.os,
                "mail": self.mail,
                "python": self.python,
                "modules": self.modules,
                "environ": self.environ,
                "project": self.project,
                "databases": self.databases,
                "installed_apps": self.installed_apps,
                "extra": self.extra,
            }
        )


config = Config(getattr(settings, "SYSINFO", {}))
