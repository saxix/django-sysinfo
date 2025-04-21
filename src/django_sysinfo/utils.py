import logging
import re
import socket
from collections import defaultdict
from importlib import metadata
from itertools import chain

import psutil
import six
from django.utils.functional import SimpleLazyObject

from django_sysinfo.conf import config

logger = logging.getLogger(__name__)


def flatten(x):
    result = []
    for el in x:
        # if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, six.string_types):
            result.extend(flatten(el))
        else:
            result.append(el)
    return list(result)


def is_valid_ip(addr):
    try:
        socket.inet_aton(addr)
        return True
    except Exception:
        return False


def humanize_bytes(data, raw=False, precision=1):
    """Return a humanized string representation of a number of bytes."""
    if raw:
        return data
    abbrevs = ((1 << 50, "PB"), (1 << 40, "TB"), (1 << 30, "GB"), (1 << 20, "MB"), (1 << 10, "kB"), (1, "bytes"))
    if data == 1:
        return "1 byte"
    factor = 0
    el = 0
    for i, (factor, __) in enumerate(abbrevs):  # pragma: no cover
        if data >= factor:
            el = i
            break
    return "%.*f %s" % (precision, data / factor, abbrevs[el][1])


def get_network(families=(socket.AF_INET,)):
    nic = psutil.net_if_addrs()

    ips = defaultdict(list)
    for card, addresses in nic.items():
        for address in addresses:
            if address.family in families:
                ips[card].append(f"{address.address}/{address.netmask}")
    return dict(ips)


def get_ips():
    return sorted(flatten(chain(get_network().values())))


def get_package_version(application_name, app=None):  # noqa
    parts = application_name.split(".")
    module_name = parts[0]
    try:
        return metadata.version(module_name)
    except Exception:  # noqa: S110
        pass
    if hasattr(app, "get_version"):
        version = app.get_version
    elif hasattr(app, "__version__"):
        version = app.__version__
    elif hasattr(app, "VERSION"):
        version = app.VERSION
    elif hasattr(app, "version"):
        version = app.version
    else:
        version = None

    if callable(version):
        try:
            version = version()
        except Exception:
            return None

    if not isinstance(version, six.string_types + (list, tuple)):
        version = None

    if version is None:
        return None

    if isinstance(version, (list | tuple)):
        version = ".".join(map(six.text_type, version))

    return six.text_type(version)


def _lazy_re_compile(regex, flags=0):
    """Lazily compile a regex with flags."""

    def _compile():
        # Compile the regex if it was not passed pre-compiled.
        if isinstance(regex, (str | bytes)):
            return re.compile(regex, flags)
        if flags:
            raise ValueError("flags must be empty if regex is passed pre-compiled")
        return regex

    return SimpleLazyObject(_compile)


def filter_environment(key, config, request):
    return key in config.hidden_environment


masked_settings = _lazy_re_compile(config.masked_environment, flags=re.IGNORECASE)
cleansed_substitute = "********************"


def cleanse_setting(key, value, config, request):
    try:
        if masked_settings.search(key):
            cleansed = f"{cleansed_substitute}{value[-3:]}"
        elif isinstance(value, dict):
            cleansed = {k: cleanse_setting(k, v) for k, v in value.items()}
        elif isinstance(value, list):
            cleansed = [cleanse_setting("", v) for v in value]
        elif isinstance(value, tuple):
            cleansed = tuple([cleanse_setting("", v) for v in value])
        else:
            cleansed = value
    except TypeError:
        # If the key isn't regex-able, just return as-is.
        cleansed = value

    return cleansed
