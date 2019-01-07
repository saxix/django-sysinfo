# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging

import pytest
from demoproject.models import test_sysinfo

from django_sysinfo.api import get_extra
from django_sysinfo.compat import reverse
from django_sysinfo.conf import config

logger = logging.getLogger(__name__)


def test_base(monkeypatch):
    monkeypatch.setattr(config, "extra", {"a": lambda x: 1,
                                          "b": "func",
                                          "c": "demoproject.models.test_sysinfo",
                                          "d": lambda x: 1.0 / 0.0,
                                          "e": test_sysinfo,
                                          })
    ret = get_extra(config)
    assert ret == {"a": 1,
                   "c": 123,
                   "e": 123,
                   }


@pytest.mark.django_db
# @pytest.mark.urls("urls")
def test_extra(client, monkeypatch):
    from demoproject.models import test_sysinfo

    monkeypatch.setattr("django_sysinfo.conf.config.host", False)
    monkeypatch.setattr("django_sysinfo.conf.config.os", False)
    monkeypatch.setattr("django_sysinfo.conf.config.python", False)
    monkeypatch.setattr("django_sysinfo.conf.config.modules", False)
    monkeypatch.setattr("django_sysinfo.conf.config.project", False)
    monkeypatch.setattr("django_sysinfo.conf.config.environ", False)
    monkeypatch.setattr("django_sysinfo.conf.config.databases", False)
    monkeypatch.setattr("django_sysinfo.conf.config.installed_apps", False)
    monkeypatch.setattr("django_sysinfo.api.config.extra", {"test1": "demoproject.models.test_sysinfo",
                                                            "test2": test_sysinfo,
                                                            })

    response = client.get(reverse("sys-info"))
    data = json.loads(response.content.decode("utf8"))
    assert list(data.keys()) == ["extra"], data.keys()
    assert data["extra"]["test1"] == 123
    assert data["extra"]["test2"] == 123


@pytest.mark.django_db
# @pytest.mark.urls("urls")
def test_extra_url(client, monkeypatch):
    from demoproject.models import test_sysinfo

    monkeypatch.setattr("django_sysinfo.conf.config.host", False)
    monkeypatch.setattr("django_sysinfo.conf.config.os", False)
    monkeypatch.setattr("django_sysinfo.conf.config.python", False)
    monkeypatch.setattr("django_sysinfo.conf.config.modules", False)
    monkeypatch.setattr("django_sysinfo.conf.config.project", False)
    monkeypatch.setattr("django_sysinfo.conf.config.environ", False)
    monkeypatch.setattr("django_sysinfo.conf.config.databases", False)
    monkeypatch.setattr("django_sysinfo.conf.config.installed_apps", False)
    monkeypatch.setattr("django_sysinfo.api.config.extra", {"test1": "demoproject.models.test_sysinfo",
                                                            "test2": test_sysinfo,
                                                            })

    response = client.get(reverse("sys-info"))
    data = json.loads(response.content.decode("utf8"))
    assert list(data.keys()) == ["extra"], data.keys()
    assert data["extra"]["test1"] == 123
    assert data["extra"]["test2"] == 123
