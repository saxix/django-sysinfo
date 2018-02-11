# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
import logging

import pytest

from django_sysinfo.api import get_checks, run_check
from django_sysinfo.compat import reverse
from django_sysinfo.conf import config

logger = logging.getLogger(__name__)


def test_base(monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": lambda x: (True, 200)})
    ret = run_check("a")
    assert ret == (True, 200)


def test_all(monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": lambda x: (True, 200),
                                           "b": "func",
                                           "c": "demoproject.models.test_check",
                                           "d": lambda x: 1.0 / 0.0,
                                           "e": 200,
                                           })
    ret = get_checks()
    assert ret == {"a": (True, 200),
                   "b": ("ERROR", 500),
                   "c": (True, 200),
                   "d": ("ERROR", 500),
                   "e": (200, 200),
                   }, ret


def test_chack_by_name(monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": "demoproject.models.test_check"})
    ret = run_check("a")
    assert ret == (True, 200)


def test_error(monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": lambda x: 1.0 / 0.0})
    ret = run_check("a")
    assert ret == ("ERROR", 500)


def test_error_raise(monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": lambda x: 1.0 / 0.0})
    with pytest.raises(ZeroDivisionError):
        run_check("a", fail_silently=False)


def test_error_custom_code(monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": lambda x: 1.0 / 0.0})
    ret = run_check("a", fail_status=404)
    assert ret == ("ERROR", 404)


@pytest.mark.django_db
# @pytest.mark.urls("urls")
def test_single_check(client, monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": lambda x: (True, 200)})
    response = client.get(reverse("sys-check", args=["a"]))
    data = json.loads(response.content.decode("utf8"))
    assert data == {"message": True}


@pytest.mark.django_db
# @pytest.mark.urls("urls")
def test_checks(client, monkeypatch):
    monkeypatch.setattr(config, "checks", {"a": lambda x: (True, 200),
                                           "b": lambda x: (False, 500),
                                           })
    response = client.get(reverse("sys-check", args=["a"]))
    data = json.loads(response.content.decode("utf8"))
    assert data == {"message": True}
