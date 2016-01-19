# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import json
import sys

import mock
import pytest
import six

import django_sysinfo.cli


class Response(object):
    c = {'databases': {'default': {'engine': 'django.db.backends.postgresql_psycopg2',
                                   'host': '127.0.0.1:',
                                   'name': 'sysinfo',
                                   'server': 'PostgreSQL 9.4.3 on x86_64-apple-darwin14.3.0, compiled by Apple LLVM version 6.1.0 (clang-602.0.53) (based on LLVM 3.6.0svn), 64-bit',
                                   'timezone': 'UTC',
                                   'version': '9.4.3'},
                       'sqlite': {'engine': 'django.db.backends.sqlite3',
                                  'host': ':',
                                  'name': ':memory:',
                                  'server': '3.8.10.2',
                                  'timezone': 'UTC',
                                  'version': '3.8.10.2'}},
         'django': [1, 9, 1, 'final', 0],
         'modules': {'alabaster': '0.7.7',
                     'apipkg': '1.4',
                     'pytest': '9.9.9',
                     'appnope': '0.1.0',
                     'xlwt-future': '0.8.0'},
         'os': {'name': 'posix',
                'uname': ['Darwin',
                          'hanarero.local',
                          '15.2.0',
                          'Darwin Kernel Version 15.2.0: Fri Nov 13 19:56:56 PST 2015; root:xnu-3248.20.55~2/RELEASE_X86_64',
                          'x86_64']},
         'process': {'memory': {'available': '1.9 GB',
                                'free': '23.1 MB',
                                'percent': '76.9 bytes',
                                'total': '8.0 GB',
                                'used': '6.0 GB'}},
         'project': {'MEDIA_ROOT': {'disk': {'free': '16.1 GB',
                                             'total': '464.8 GB',
                                             'used': '448.4 GB'},
                                    'path': 'django-sysinfo/tests/demo/demoproject/media'},
                     'STATIC_ROOT': {'disk': {'free': '16.1 GB',
                                              'total': '464.8 GB',
                                              'used': '448.4 GB'},
                                     'location': '/django-sysinfo/tests/demo/demoproject/static'},
                     'current_dir': 'django-sysinfo/tests/demo',
                     'installed_apps': [['django_sysinfo', '0.1a20160115214246']],
                     'tempdir': '/jjqmc4bj38z2rj90qzhwsczw0000gn/T'},
         'python': {'executable': '/data/VENV/django-sysinfo/bin/python',
                    'info': '2.7.10 (default, Jan  5 2016, 19:33:10) \n[GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)]',
                    'platform': 'darwin',
                    'version': '2.7.10'}}

    def json(self):
        return self.c

    @property
    def content(self):
        return json.dumps(self.c)


class Version(object):
    c = {'pytest': '9.9.9'}

    def json(self):
        return self.c

    @property
    def content(self):
        return json.dumps(self.c)


@pytest.fixture
def response():
    return Response()


@pytest.fixture
def version():
    return Version()


def test_raw(monkeypatch, response):
    out = six.StringIO()
    monkeypatch.setattr(sys, 'exit', mock.Mock())

    sys.argv = ["django-sysinfo", "localhost", "--raw"]
    with mock.patch('requests.get', return_value=response):
        django_sysinfo.cli.main(stdout=out)
    out.seek(0)
    content = out.read()
    res = json.loads(content, 'utf-8')
    assert res['django']


def test_format(monkeypatch, response):
    out = six.StringIO()
    monkeypatch.setattr(sys, 'exit', mock.Mock())

    sys.argv = ["django-sysinfo", "localhost"]
    with mock.patch('requests.get', return_value=response):
        django_sysinfo.cli.main(stdout=out)
    out.seek(0)
    assert 'databases' in out.read()


def test_module(monkeypatch, version):
    out = six.StringIO()
    monkeypatch.setattr(sys, 'exit', mock.Mock())

    sys.argv = ["django-sysinfo", "localhost", "--module", "pytest"]
    with mock.patch('requests.get', return_value=version):
        django_sysinfo.cli.main(stdout=out)
    out.seek(0)
    assert out.read()[:-1] == version.c['pytest']


def test_exclude(monkeypatch, response):
    out = six.StringIO()
    monkeypatch.setattr(sys, 'exit', mock.Mock())

    sys.argv = ["django-sysinfo", "localhost", "--exclude", "databases,modules,os,process,project,python"]
    with mock.patch('requests.get', return_value=response):
        django_sysinfo.cli.main(stdout=out)
    out.seek(0)
    assert out.read()[:-1] == "{'django': [1, 9, 1, 'final', 0]}"


def test_include(monkeypatch, response):
    out = six.StringIO()
    monkeypatch.setattr(sys, 'exit', mock.Mock())

    sys.argv = ["django-sysinfo", "localhost", "--only", "os.name"]
    with mock.patch('requests.get', return_value=response):
        django_sysinfo.cli.main(stdout=out)
    out.seek(0)
    assert out.read()[:-1] == "{'os.name': 'posix'}"
