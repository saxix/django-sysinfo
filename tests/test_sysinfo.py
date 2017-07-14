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
        user = User(username="sax", email="")
        user.set_password("123")
        user.save()
    except IntegrityError:
        pass
    return user


@pytest.mark.django_db
@pytest.mark.urls("urls")
def test_sysinfo(client, cache):
    response = client.get(reverse("sys-info"))
    data = json.loads(response.content.decode("utf8"))

    assert data["modules"]["pytest"] == pytest.__version__


@pytest.mark.django_db
@pytest.mark.urls("urls")
def test_echo(client, cache):
    response = client.get(reverse("sys-echo", args=["abc"]))
    assert response.content.decode("utf8") == "abc"


@pytest.mark.django_db
@pytest.mark.urls("urls")
def test_sysinfo_limit_Sections(client, cache):
    response = client.get("%s?s=os,host" % reverse("sys-info"))
    data = json.loads(response.content.decode("utf8"))

    assert sorted(data.keys()) == ["host", "os"]


@pytest.mark.django_db
def test_http_basic(rf, user, monkeypatch, settings):
    import base64
    settings.SYSINFO_USERS = [user.username]

    monkeypatch.setattr("django.contrib.auth.login", lambda r, u: True)
    f = http_basic_auth(lambda r: "OK")

    auth_headers = {"HTTP_AUTHORIZATION": b"Basic " + base64.b64encode("username:password".encode())}
    r = rf.get("/", **auth_headers)
    with pytest.raises(PermissionDenied):
        f(r)

    auth_headers = {"HTTP_AUTHORIZATION": b"Basic " + base64.b64encode("sax:123".encode())}
    r = rf.get("/", **auth_headers)
    assert f(r) == "OK"


@pytest.mark.django_db
def test_http_basic_login(client):
    response = client.get(reverse("sys-info-auth"))
    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.urls("urls")
def test_version(client):
    response = client.get(reverse("sys-version", args=["pytest"]))
    data = json.loads(response.content.decode("utf8"))
    assert data["pytest"] == pytest.__version__


@pytest.mark.django_db
@pytest.mark.urls("urls")
def test_version_wrong(client):
    response = client.get(reverse("sys-version", args=["@@@"]))
    data = json.loads(response.content.decode("utf8"))
    assert data["@@@"] == UNKNOWN
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.urls("urls")
def test_config(client, monkeypatch):
    monkeypatch.setattr("django_sysinfo.conf.config.host", False)
    monkeypatch.setattr("django_sysinfo.conf.config.os", False)
    monkeypatch.setattr("django_sysinfo.conf.config.python", False)
    monkeypatch.setattr("django_sysinfo.conf.config.modules", False)
    monkeypatch.setattr("django_sysinfo.conf.config.project", False)
    monkeypatch.setattr("django_sysinfo.conf.config.databases", False)
    monkeypatch.setattr("django_sysinfo.conf.config.extra", False)
    monkeypatch.setattr("django_sysinfo.conf.config.checks", False)

    response = client.get(reverse("sys-info"))
    data = json.loads(response.content.decode("utf8"))
    assert data == {}, data
