import socket
from collections import namedtuple
from unittest import mock

from mock_import import mock_import

from django_sysinfo.utils import flatten, get_ips, get_network, get_package_version, humanize_bytes, is_valid_ip


def test_get_network():
    snic = namedtuple("snic", ["family", "address", "netmask", "broadcast", "ptp"])
    mocked = {
        "awdl0": [
            snic(
                family=30,
                address="fe80::3854:80ff:fe54:7bf8%awdl0",
                netmask="ffff:ffff:ffff:ffff::",
                broadcast=None,
                ptp=None,
            )
        ],
        "en0": [
            snic(family=2, address="192.168.10.200", netmask="255.255.255.0", broadcast="192.168.10.255", ptp=None),
            snic(
                family=30,
                address="fe80::6e40:8ff:feac:4f94%en0",
                netmask="ffff:ffff:ffff:ffff::",
                broadcast=None,
                ptp=None,
            ),
        ],
        "bridge0": [snic(family=18, address="6e:40:08:ca:60:00", netmask=None, broadcast=None, ptp=None)],
        "lo0": [
            snic(family=2, address="127.0.0.1", netmask="255.0.0.0", broadcast=None, ptp=None),
            snic(family=30, address="fe80::1%lo0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None),
        ],
    }
    with mock.patch("psutil.net_if_addrs", side_effect=lambda: mocked):
        data_inet = get_network([socket.AF_INET])
    assert sorted(data_inet.keys()) == ["en0", "lo0"]

    with mock.patch("psutil.net_if_addrs", side_effect=lambda: mocked):
        assert sorted(data_inet.values()) == [["127.0.0.1/255.0.0.0"], ["192.168.10.200/255.255.255.0"]]


def test_get_ips():
    snic = namedtuple("snic", ["family", "address", "netmask", "broadcast", "ptp"])
    mocked = {
        "awdl0": [
            snic(
                family=30,
                address="fe80::3854:80ff:fe54:7bf8%awdl0",
                netmask="ffff:ffff:ffff:ffff::",
                broadcast=None,
                ptp=None,
            )
        ],
        "en0": [
            snic(family=2, address="192.168.10.200", netmask="255.255.255.0", broadcast="192.168.10.255", ptp=None),
            snic(
                family=30,
                address="fe80::6e40:8ff:feac:4f94%en0",
                netmask="ffff:ffff:ffff:ffff::",
                broadcast=None,
                ptp=None,
            ),
        ],
        "bridge0": [snic(family=18, address="6e:40:08:ca:60:00", netmask=None, broadcast=None, ptp=None)],
        "lo0": [
            snic(family=2, address="127.0.0.1", netmask="255.0.0.0", broadcast=None, ptp=None),
            snic(family=30, address="fe80::1%lo0", netmask="ffff:ffff:ffff:ffff::", broadcast=None, ptp=None),
        ],
    }
    with mock.patch("psutil.net_if_addrs", side_effect=lambda: mocked):
        assert get_ips() == ["127.0.0.1/255.0.0.0", "192.168.10.200/255.255.255.0"]


def test_get_package_version():
    with mock_import(spec={"VERSION"}):
        import my_module

        my_module.VERSION = "1.0"
        assert get_package_version("my_module", my_module) == "1.0"

    with mock_import(spec=["VERSION"], VERSION="1.0"):
        import my_module

        assert get_package_version("my_module", my_module) == "1.0"

    with mock_import(spec=["__version__"], __version__="1.1"):
        import my_module

        assert get_package_version("my_module", my_module) == "1.1"

    with mock_import(spec=["get_version"], get_version=lambda: "1.2"):
        import my_module

        assert get_package_version("my_module", my_module) == "1.2"

    with mock_import(spec=["get_version"], get_version=mock.MagicMock(side_effect=Exception)):
        import my_module

        assert get_package_version("my_module", my_module) is None

    with mock_import(spec=["version"], version="1.3"):
        import my_module

        assert get_package_version("my_module", my_module) == "1.3"

    with mock_import(spec=["VERSION"], VERSION=[1, 4]):
        import my_module

        assert get_package_version("my_module", my_module) == "1.4"

    with mock_import(spec=["VERSION"], VERSION=None):
        import my_module

        assert get_package_version("my_module", my_module) is None

    with mock_import(spec=[]):
        import my_module

        assert get_package_version("my_module", my_module) is None


def test_humanize_bytes():
    assert humanize_bytes(1) == "1 byte"
    assert humanize_bytes(2) == "2.0 bytes"
    assert humanize_bytes(1024) == "1.0 kB"
    assert humanize_bytes(1024 * 123) == "123.0 kB"
    assert humanize_bytes(1024 * 12342) == "12.1 MB"
    assert humanize_bytes(1024 * 12342, precision=2) == "12.05 MB"
    assert humanize_bytes(1024 * 1234, precision=2) == "1.21 MB"
    assert humanize_bytes(1024 * 1234 * 1111, precision=2) == "1.31 GB"
    assert humanize_bytes(1024 * 1234 * 1111) == "1.3 GB"
    assert humanize_bytes(1024, True) == 1024


def test_is_valid_ip():
    assert not is_valid_ip("127.0.0.300")
    assert is_valid_ip("127.0.0.1")


def test_flatten():
    assert flatten([1, 2, [3, 4], (5, 6)]) == [1, 2, 3, 4, 5, 6]
    assert flatten([[[1, 2, 3], (42, None)], [4, 5], [6], 7, (8, 9, 10)]) == [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]
