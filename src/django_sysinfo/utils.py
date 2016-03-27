# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging
import psutil
import socket
from collections import defaultdict
from itertools import chain

import six

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
    try:
        socket.inet_aton(addr)
        return True
    except Exception:
        return False


def humanize_bytes(bytes, raw=False, precision=1):
    u"""Return a humanized string representation of a number of bytes.

    Assumes `from __future__ import division`.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    if raw:
        return bytes
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)


def get_network(families=[socket.AF_INET]):
    """
    >>> import mock
    >>> from psutil._common import snic
    >>> MOCK = {
    ... 'awdl0': [snic(family=30, address='fe80::3854:80ff:fe54:7bf8%awdl0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)],
    ... 'en0':   [snic(family=2, address='192.168.10.200', netmask='255.255.255.0', broadcast='192.168.10.255', ptp=None),
    ...           snic(family=30, address='fe80::6e40:8ff:feac:4f94%en0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)],
    ... 'bridge0': [snic(family=18, address='6e:40:08:ca:60:00', netmask=None, broadcast=None, ptp=None)],
    ... 'lo0': [snic(family=30, address='::1', netmask='ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', broadcast=None, ptp=None),
    ...         snic(family=30, address='fe80::1%lo0', netmask='ffff:ffff:ffff:ffff::', broadcast=None, ptp=None)]}

    >>> mock.patch('psutil.net_if_addrs', MOCK)  # doctest:+ELIPSIS
    ...
    >>> data_inet = get_network()
    >>> sorted(data_inet.keys())
    ['en0', 'lo0']
    >>> sorted(data_inet.values())
    [[u'127.0.0.1/255.0.0.0'], [u'192.168.10.200/255.255.255.0']]

    >>> data_inet6 = get_network([socket.AF_INET6])
    >>> sorted(flatten(data_inet6.values()))
    [u'::1/ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', u'fe80::1%lo0/ffff:ffff:ffff:ffff::', u'fe80::3854:80ff:fe54:7bf8%awdl0/ffff:ffff:ffff:ffff::', u'fe80::6e40:8ff:feac:4f94%en0/ffff:ffff:ffff:ffff::']
    """
    nic = psutil.net_if_addrs()
    ips = defaultdict(list)
    # return nic
    for card, addresses in nic.items():
        for address in addresses:
            if address.family in families:
                ips[card].append("{0.address}/{0.netmask}".format(address))
    return dict(ips)
    # return flatten([[d.address for d in data if is_valid_ip(d)] for card, data in nic.items()])


def get_ips():
    """
    >>> get_ips()
    [u'127.0.0.1/255.0.0.0', u'192.168.10.200/255.255.255.0']
    """
    return sorted(flatten(chain(get_network().values())))
