# # -*- coding: utf-8 -*-
# from __future__ import absolute_import, unicode_literals
#
# import logging
# import socket
#
# from django.utils.translation import gettext as _
#
# from django_sysinfo.utils import get_network, flatten
#
# logger = logging.getLogger(__name__)
#
#
# def test_get_network(monkeypatch):
#     from psutil._common import snic
#     import mock
#     MOCK = {
#         # "awdl0": [
#         #     snic(family=30, address="fe80::3854:80ff:fe54:7bf8%awdl0", netmask="ffff:ffff:ffff:ffff::", broadcast=None,
#         #          ptp=None)],
#         "en1": [snic(family=2, address="192.168.10.200", netmask="255.255.255.0", broadcast="192.168.10.255", ptp=None),
#                 snic(family=30, address="addr:en1", netmask="net:mask:en1", broadcast=None,
#                      ptp=None)
#                 ],
#         # "bridge0": [snic(family=18, address="6e:40:08:ca:60:00", netmask=None, broadcast=None, ptp=None)],
#         "lo1": [
#             snic(family=2, address="127.0.0.1", netmask="255.0.0.0", broadcast=None, ptp=None),
#             snic(family=30, address="addr:lo1", netmask="net:mask:lo1", broadcast=None, ptp=None)
#         ]
#     }
#     # monkeypatch.setattr("psutil.net_if_addrs", lambda: MOCK)
#     with mock.patch("psutil.net_if_addrs", side_effect=lambda: MOCK):
#     # with mock.patch("psutil.net_if_addrs", MOCK):
#         data_inet = get_network()
#         assert sorted(data_inet.keys()) == ['en1', 'lo1']
#         assert sorted(data_inet.values()) == [['127.0.0.1/255.0.0.0'],
#                                               ['192.168.10.200/255.255.255.0']]
#
#         data_inet6 = get_network([socket.AF_INET6])
#         assert sorted(flatten(data_inet6.values())) == ['addr:en1/net:mask:en1',
#                                                         'addr:lo1/net:mask:lo1',
#                                                         ]
