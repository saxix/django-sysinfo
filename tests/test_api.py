# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import logging

import pytest
from django.db import connections

from django_sysinfo.api import get_databases

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_broken_database(settings, monkeypatch):
    settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:"},

        "broken": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "not-existent-db",
            "HOST": "127.0.0.1",
            "PORT": "21",
            "USER": "",
            "PASSWORD": ""},

    }
    monkeypatch.setattr(connections, "_databases", None)
    del connections.databases

    ret = get_databases()
    assert sorted(ret.keys()) == ["broken", "default"]
    # assert ret["default"]["engine"] == "django.db.backends.sqlite3"
    assert ret["broken"]["engine"] == "django.db.backends.postgresql_psycopg2"
    assert ret["broken"]["host"] == "127.0.0.1:21"
    assert ret["broken"]["name"] == "not-existent-db"
    assert ret["broken"]["error"] == """could not connect to server: Connection refused
\tIs the server running on host "127.0.0.1" and accepting
\tTCP/IP connections on port 21?
"""
