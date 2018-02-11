# -*- coding: utf-8 -*-

import pytest

from django_sysinfo.compat import reverse


@pytest.mark.django_db
def test_sysinfo(django_app, admin_user):
    response = django_app.get(reverse("sys-admin-info"),
                          user=admin_user.username)
    assert response.status_code == 200
