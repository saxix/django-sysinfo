# -*- coding: utf-8 -*-
import logging
import os

import pkg_resources
import psutil
import socket
from collections import defaultdict
from itertools import chain

import six

from django_sysinfo.conf import config

logger = logging.getLogger(__name__)


def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:

    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]

    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, (8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        # if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, six.string_types):
            result.extend(flatten(el))
        else:
            result.append(el)
    return list(result)


def is_valid_ip(addr):
    """
    check if addr is a valid ip4 address

    >>> is_valid_ip('127.0.0.300')
    False
    >>> is_valid_ip('127.0.0.1')
    True
    """
    try:
        socket.inet_aton(addr)
        return True
    except Exception:
        return False


def humanize_bytes(bytes, raw=False, precision=1):
    """Return a humanized string representation of a number of bytes.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(2)
    '2.0 bytes'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342, precision=2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234, precision=2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111, precision=2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111)
    '1.3 GB'
    >>> humanize_bytes(1024, True)
    1024
    """
    if raw:
        return bytes
    abbrevs = (
        (1 << 50, "PB"),
        (1 << 40, "TB"),
        (1 << 30, "GB"),
        (1 << 20, "MB"),
        (1 << 10, "kB"),
        (1, "bytes")
    )
    if bytes == 1:
        return "1 byte"
    for factor, suffix in abbrevs:  # pragma: no cover
        if bytes >= factor:
            break
    return "%.*f %s" % (precision, bytes / factor, suffix)


def get_network(families=[socket.AF_INET]):
    """
    # >>> from psutil._common import snic
    >>> import mock
    >>> from collections import namedtuple
    >>> snic = namedtuple('snic', ['family', 'address', 'netmask', 'broadcast', 'ptp'])
    >>> MOCK = {
    ... "awdl0": [snic(family=30, address="fe80::3854:80ff:fe54:7bf8%awdl0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None)],
    ... "en0":   [snic(family=2, address="192.168.10.200", netmask="255.255.255.0", broadcast="192.168.10.255", ptp=None),
    ...           snic(family=30, address="fe80::6e40:8ff:feac:4f94%en0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None)],
    ... "bridge0": [snic(family=18, address="6e:40:08:ca:60:00", netmask=None, broadcast=None, ptp=None)],
    ... "lo0": [snic(family=2, address="127.0.0.1", netmask="255.0.0.0", broadcast=None, ptp=None),
    ...         snic(family=30, address="fe80::1%lo0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None)]}

    >>> with mock.patch("psutil.net_if_addrs", side_effect=lambda: MOCK):
    ...     data_inet = get_network([socket.AF_INET])
    ...     sorted(data_inet.keys())
    ['en0', 'lo0']

    >>> with mock.patch("psutil.net_if_addrs", side_effect=lambda: MOCK):
    ...     sorted(data_inet.values())
    [[u'127.0.0.1/255.0.0.0'], [u'192.168.10.200/255.255.255.0']]

    """
    nic = psutil.net_if_addrs()

    ips = defaultdict(list)
    for card, addresses in nic.items():
        for address in addresses:
            if address.family in families:
                ips[card].append("{0.address}/{0.netmask}".format(address))
    return dict(ips)
    # return flatten([[d.address for d in data if is_valid_ip(d)] for card, data in nic.items()])


def get_ips():
    """
    >>> import mock
    >>> from collections import namedtuple
    >>> snic = namedtuple('snic', ['family', 'address', 'netmask', 'broadcast', 'ptp'])
    >>> MOCK = {
    ... "awdl0": [snic(family=30, address="fe80::3854:80ff:fe54:7bf8%awdl0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None)],
    ... "en0":   [snic(family=2, address="192.168.10.200", netmask="255.255.255.0", broadcast="192.168.10.255", ptp=None),
    ...           snic(family=30, address="fe80::6e40:8ff:feac:4f94%en0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None)],
    ... "bridge0": [snic(family=18, address="6e:40:08:ca:60:00", netmask=None, broadcast=None, ptp=None)],
    ... "lo0": [snic(family=2, address="127.0.0.1", netmask="255.0.0.0", broadcast=None, ptp=None),
    ...         snic(family=30, address="fe80::1%lo0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None)]}
    >>> with mock.patch("psutil.net_if_addrs", side_effect=lambda: MOCK):
    ...     get_ips()
    ['127.0.0.1/255.0.0.0', '192.168.10.200/255.255.255.0']
    """
    return sorted(flatten(chain(get_network().values())))


def get_package_version(application_name, app=None):  # noqa
    """
    # >>> get_package_version('django_sysinfo') == django_sysinfo.__version__
    # True
    # >>> with mock.patch('pkg_resources.get_distribution', None):
    # ...     get_package_version('django_sysinfo') == django_sysinfo.__version__
    # True

    :param application_name:
    :param app:
    :return:

    >>> import django_sysinfo, mock
    >>> from mock_import import mock_import
    >>> with mock_import(spec={'VERSION'}):
    ...     import my_module
    ...     my_module.VERSION = '1.0'
    ...     assert get_package_version('my_module', my_module) == '1.0'


    >>> with mock_import(spec=['VERSION'],VERSION='1.0'):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) == '1.0'

    >>> with mock_import(spec=['__version__'], __version__='1.1'):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) == '1.1'

    >>> with mock_import(spec=['get_version'], get_version=lambda : '1.2'):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) == '1.2'

    >>> with mock_import(spec=['get_version'], get_version=mock.MagicMock(side_effect=Exception)):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) is None

    >>> with mock_import(spec=['version'], version='1.3'):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) == '1.3'

    >>> with mock_import(spec=['VERSION'], VERSION=[1,4]):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) == '1.4'

    >>> with mock_import(spec=['VERSION'], VERSION=None):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) is None

    >>> with mock_import(spec=[]):
    ...     import my_module
    ...     assert get_package_version('my_module', my_module) is None
    """

    parts = application_name.split('.')
    module_name = parts[0]
    try:
        return pkg_resources.get_distribution(module_name).version
    except Exception:
        pass
    # if app is None:
    #     app = __import__(module_name)
    if hasattr(app, 'get_version'):
        version = app.get_version
    elif hasattr(app, '__version__'):
        version = app.__version__
    elif hasattr(app, 'VERSION'):
        version = app.VERSION
    elif hasattr(app, 'version'):
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

    if isinstance(version, (list, tuple)):
        version = '.'.join(map(six.text_type, version))

    return six.text_type(version)

# def get_all_package_versions():
#     packages = {}
#     for module_name, app in sys.modules.items():
#         # ignore items that look like submodules
#         if '.' in module_name:
#             continue
#
#         if 'sys' == module_name:
#             continue
#
#         version = get_package_version(module_name, app)
#
#         if version is None:
#             continue
#
#         packages[module_name.lower()] = version
#
#     packages['sys'] = '{0}.{1}.{2}'.format(*sys.version_info)
#
#     return OrderedDict(sorted(packages.items()))

def filter_environment(key):
    if key in config.masked_environment:
        return "****"
    return os.environ['key']
