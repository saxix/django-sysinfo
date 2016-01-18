# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
import logging

import pytest
from django.core.urlresolvers import reverse

from django_sysinfo.api import UNKNOWN

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_sysinfo(client):
    response = client.get(reverse('sys-info'))
    data = json.loads(response.content.decode('utf8'))

    assert data['modules']['pytest'] == pytest.__version__


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
