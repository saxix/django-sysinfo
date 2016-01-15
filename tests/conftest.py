# import sys
# import django
# import pytest
#
#
# @pytest.fixture(scope='session')
# def client(request):
#     import django_webtest
#     wtm = django_webtest.WebTestMixin()
#     wtm.csrf_checks = False
#     wtm._patch_settings()
#     request.addfinalizer(wtm._unpatch_settings)
#     app = django_webtest.DjangoTestApp()
#     return app
