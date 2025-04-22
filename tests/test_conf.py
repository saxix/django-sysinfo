from django_sysinfo.conf import Config, merge


def test_merge():
    a = {1: {"a": "A"}, 2: {"b": "B"}, 8: []}
    b = {2: {"c": "C"}, 3: {"d": "D"}}
    c = merge(a, b)
    assert c == a == {8: [], 1: {"a": "A"}, 2: {"c": "C", "b": "B"}, 3: {"d": "D"}}

    c = merge(a, {1: "a"})
    assert c[1] == "a"


def test_config():
    c = Config({"os": False})
    assert (c.os, c.python, c.project["mail"], c.MEDIA_ROOT) == (False, True, True, True)
    c = Config({"os": True, "installed_apps": False})
    assert not c.installed_apps
