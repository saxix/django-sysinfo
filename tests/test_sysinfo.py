# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging

import pytest
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from django_sysinfo.api import UNKNOWN
from django_sysinfo.views import http_basic_auth

logger = logging.getLogger(__name__)


@pytest.fixture
def user(db):
    from django.contrib.auth.models import User
    from django.db import IntegrityError

    try:
        user = User(username='sax', email='')
        user.set_password('123')
        user.save()
    except IntegrityError:
        pass


@pytest.mark.django_db
def test_sysinfo(client):
    response = client.get(reverse('sys-info'))
    data = json.loads(response.content.decode('utf8'))

    assert data['modules']['pytest'] == pytest.__version__


@pytest.mark.django_db
def test_http_basic(rf, user, monkeypatch):
    import base64

    monkeypatch.setattr('django.contrib.auth.login', lambda r, u: True)
    f = http_basic_auth(lambda r: 'OK')

    auth_headers = {'HTTP_AUTHORIZATION': b'Basic ' + base64.b64encode('username:password'.encode())}
    r = rf.get('/', **auth_headers)
    with pytest.raises(PermissionDenied):
        f(r)

    auth_headers = {'HTTP_AUTHORIZATION': b'Basic ' + base64.b64encode('sax:123'.encode())}
    r = rf.get('/', **auth_headers)
    assert f(r) == 'OK'


@pytest.mark.django_db
def test_http_basic_login(client):
    response = client.get(reverse('sys-info-auth'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_version(client):
    response = client.get(reverse('sys-version', args=['pytest']))
    data = json.loads(response.content.decode('utf8'))
    assert data['pytest'] == pytest.__version__


@pytest.mark.django_db
def test_version_wrong(client):
    response = client.get(reverse('sys-version', args=['@@@']))
    data = json.loads(response.content.decode('utf8'))
    assert data['@@@'] == UNKNOWN
    assert response.status_code == 404
