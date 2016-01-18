# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
import sys

import mock
import six

import django_sysinfo.cli


class Response(object):
    c = {u'databases': {u'default': {u'engine': u'django.db.backends.postgresql_psycopg2',
                                     u'host': u'127.0.0.1:',
                                     u'name': u'sysinfo',
                                     u'server': u'PostgreSQL 9.4.3 on x86_64-apple-darwin14.3.0, compiled by Apple LLVM version 6.1.0 (clang-602.0.53) (based on LLVM 3.6.0svn), 64-bit',
                                     u'timezone': u'UTC',
                                     u'version': u'9.4.3'},
                        u'sqlite': {u'engine': u'django.db.backends.sqlite3',
                                    u'host': u':',
                                    u'name': u':memory:',
                                    u'server': u'3.8.10.2',
                                    u'timezone': u'UTC',
                                    u'version': u'3.8.10.2'}},
         u'django': [1, 9, 1, u'final', 0],
         u'modules': {u'alabaster': u'0.7.7',
                      u'apipkg': u'1.4',
                      u'appnope': u'0.1.0',
                      u'xlwt-future': u'0.8.0'},
         u'os': {u'name': u'posix',
                 u'uname': [u'Darwin',
                            u'hanarero.local',
                            u'15.2.0',
                            u'Darwin Kernel Version 15.2.0: Fri Nov 13 19:56:56 PST 2015; root:xnu-3248.20.55~2/RELEASE_X86_64',
                            u'x86_64']},
         u'process': {u'memory': {u'available': u'1.9 GB',
                                  u'free': u'23.1 MB',
                                  u'percent': u'76.9 bytes',
                                  u'total': u'8.0 GB',
                                  u'used': u'6.0 GB'}},
         u'project': {u'MEDIA_ROOT': {u'disk': {u'free': u'16.1 GB',
                                                u'total': u'464.8 GB',
                                                u'used': u'448.4 GB'},
                                      u'path': u'django-sysinfo/tests/demo/demoproject/media'},
                      u'STATIC_ROOT': {u'disk': {u'free': u'16.1 GB',
                                                 u'total': u'464.8 GB',
                                                 u'used': u'448.4 GB'},
                                       u'location': u'/django-sysinfo/tests/demo/demoproject/static'},
                      u'current_dir': u'django-sysinfo/tests/demo',
                      u'installed_apps': [[u'django_sysinfo', u'0.1a20160115214246']],
                      u'tempdir': u'/jjqmc4bj38z2rj90qzhwsczw0000gn/T'},
         u'python': {u'executable': u'/data/VENV/django-sysinfo/bin/python',
                     u'info': u'2.7.10 (default, Jan  5 2016, 19:33:10) \n[GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)]',
                     u'platform': u'darwin',
                     u'version': u'2.7.10'}}

    def json(self):
        return self.c

    @property
    def content(self):
        return json.dumps(self.c)


def test_get(monkeypatch):
    out = six.StringIO()

    monkeypatch.setattr(sys, 'exit', mock.Mock())

    sys.argv = ["django-sysinfo", "localhost", "--raw"]
    with mock.patch('requests.get', return_value=Response()):
        django_sysinfo.cli.main(stdout=out)
    out.seek(0)
    content = out.read()
    res = json.loads(content, 'utf-8')
    assert res['django']
