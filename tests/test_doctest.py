import doctest
import pkgutil
from io import StringIO

import pytest

import django_sysinfo as package

finder = doctest.DocTestFinder(exclude_empty=True)

pytestmarker = pytest.mark.trylast


def pytest_generate_tests(metafunc):
    if "test" in metafunc.fixturenames:
        tests = []
        ids = []
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                              prefix=package.__name__ + ".",
                                                              onerror=lambda x: None):
            try:
                m = __import__(modname, fromlist="dummy")
                if finder.find(m, modname, globs=None, extraglobs=None):
                    tests.append(m)
                    ids.append(modname)
            except Exception:
                pass
        metafunc.parametrize("test", tests, ids=ids)


def test_doctest(test):
    runner = doctest.DocTestRunner(verbose=0, optionflags=0)
    io = StringIO()
    for t in finder.find(test, test.__name__):
        runner.run(t, out=io.write, clear_globs=True)
        if runner.failures:
            io.seek(0)
            msg = io.read()
            raise Exception(msg)
