from django.db import connections

import logging
import pytest
from collections import OrderedDict

from django_sysinfo.api import get_databases, get_mail

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_database():
    ret = get_databases()
    assert ret['default']['engine'] == 'django.db.backends.postgresql_psycopg2'
    assert ret['sqlite']['engine'] == 'django.db.backends.sqlite3'


@pytest.mark.django_db
def test_mail():
    ret = get_mail()
    assert ret == OrderedDict([("backend", "django.core.mail.backends.locmem.EmailBackend"),
                               ("host", "localhost:25"),
                               ("tls", False), ("ssl", False),
                               ("status", "OK")]), ret


@pytest.mark.django_db
def test_mail_broken(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    ret = get_mail()
    assert ret["status"] in ("[Errno 61] Connection refused",
                             "[Errno 111] Connection refused"), ret


@pytest.mark.django_db
@pytest.mark.filterwarnings('ignore:Overriding setting DATABASES')
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
            "PASSWORD": ""
        },

    }

    # monkeypatch ConnectionHandler
    if hasattr(connections, 'settings'):
        monkeypatch.setattr(connections, "_settings", None, raising=False)  # dj>=3.2
        del connections.settings
    elif hasattr(connections, 'databases'):
        monkeypatch.setattr(connections, "_databases", None, raising=False)  # dj<3.2
        del connections.databases

    ret = get_databases()
    assert sorted(ret.keys()) == ["broken", "default"]
    assert ret["broken"]["engine"] == "django.db.backends.postgresql_psycopg2"
    assert ret["broken"]["host"] == "127.0.0.1:21"
    assert ret["broken"]["name"] == "not-existent-db"
