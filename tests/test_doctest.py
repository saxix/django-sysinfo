# # -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function
#
# import doctest
# import pkgutil
# from io import BytesIO
#
# import pytest
#
# import django_sysinfo
#
# finder = doctest.DocTestFinder(exclude_empty=True)
#
# pytestmarker = pytest.mark.trylast
#
#
# def pytest_generate_tests(metafunc):
#     if "test" in metafunc.fixturenames:
#         tests = []
#         ids = []
#         for importer, modname, ispkg in pkgutil.walk_packages(path=django_sysinfo.__path__,
#                                                               prefix=django_sysinfo.__name__ + ".",
#                                                               onerror=lambda x: None):
#             m = __import__(modname, fromlist="dummy")
#             if finder.find(m, modname, globs=None, extraglobs=None):
#                 tests.append(m)
#                 ids.append(modname)
#
#         metafunc.parametrize("test", tests, ids=ids)
#
#
# def test_doctest(test):
#     compare = doctest.ELLIPSIS + doctest.IGNORE_EXCEPTION_DETAIL
#     runner = doctest.DocTestRunner(verbose=0, optionflags=compare)
#     io = BytesIO()
#     for t in finder.find(test, test.__name__):
#         runner.run(t, out=io.write, clear_globs=True)
#         if runner.failures:
#             io.seek(0)
#             msg = io.read()
#             raise Exception(msg)
