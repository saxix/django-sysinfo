# -*- coding: utf-8 -*-
"""
Andy (c) 2015 UN World Food Programme

Usage:
    django-sysinfo <host> ...
                    [--username=USERNAME] [--password=PASSWORD]
                    [--debug] [--raw]
                    [--module=MODULE]
                    [--only=SECTIONS]
                    [--exclude=SECTIONS]



Options:
    -h --help               Show this screen.
    --version               Show version.
    --module MODULE         only print MODULE version

"""
# [--server=SERVER] [--timeout=TIMEOUT]
# [--username=USERNAME] [--password=PASSWORD]
# [--debug]
# andy (get|filter|sql|code|meta) <url> [FILTER ...]
#         [--timeout=TIMEOUT] [--format=FORMAT]
#         [--username=USERNAME] [--password=PASSWORD]
#         [--server=SERVER]
#         [--debug] [--raw] [-vvv]
# andy (-h | --help)
# andy --version
#
# Options:
#     -h --help               Show this screen.
#     --version               Show version.
#     --timeout TIMEOUT       Timeout [default: 10]
#     --format FORMAT         Output format [default: json]
#     --server SERVER         Output format [default: http://api.wfp.org]
#     -u --username USERNAME  Username
#     -p --password PASSWORD  Password
#     --debug                 debug
#     --raw                   raw response
# Examples:
#
#     andy get gtd/contact last_name=apostolico

# """
from __future__ import absolute_import, print_function, unicode_literals

import os
import pprint
import sys

import requests
import six
from docopt import docopt

import django_sysinfo as me

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


if six.PY2:
    import ConfigParser as configparser
else:
    import configparser
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def printout(text, colour=WHITE):
    sys.stdout.write(text)


if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
    try:
        import curses

        curses.setupterm()
        if curses.tigetnum("colors") > 2:
            def printout(text, colour=WHITE):  # noqa
                seq = "\x1b[1;%dm" % (30 + colour) + text + "\x1b[0m"
                sys.stdout.write(seq)

    except:
        # guess false in case of error
        pass


def help():
    print('')


def read_credential(target):
    cfgfile = os.path.expanduser("~/.django_sysinfo.cfg")
    try:
        config = configparser.ConfigParser()
        config.read(cfgfile)
        return config.get(target, 'username'), config.get(target, 'password')
    except (configparser.NoSectionError, configparser.NoOptionError):
        return None, None


class dotdictify(dict):
    def __init__(self, value=None):
        if isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])

    def __setitem__(self, key, value):
        if '.' in key:
            myKey, restOfKey = key.split('.', 1)
            target = self.setdefault(myKey, dotdictify())
            # if not isinstance(target, dotdictify):
            #     raise KeyError('cannot set "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target)))
            target[restOfKey] = value
        else:
            if isinstance(value, dict) and not isinstance(value, dotdictify):
                value = dotdictify(value)
            dict.__setitem__(self, key, value)

    def has_key(self, k):
        return k in self

    def __getitem__(self, key):
        if '.' not in key:
            return dict.__getitem__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        return target[restOfKey]

    def __contains__(self, key):
        if '.' not in key:
            return dict.__contains__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        return restOfKey in target

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    __setattr__ = __setitem__
    __getattr__ = __getitem__


def main(args=None, stdout=sys.stdout):  # noqa

    args = docopt(__doc__, args, version='django-sysinfo {}'.format(me.get_version()))
    hosts = args['<host>']
    # debug = args['--debug']
    module = args['--module']
    raw = args['--raw']
    only = args['--only'] or ''
    exclude = args['--exclude'] or ''
    if not isinstance(hosts, (list, tuple)):
        hosts = [hosts]

    for param in hosts:
        try:
            if not param.startswith('http://'):
                param = 'http://' + param
            o = urlparse(param)
            scheme = o.scheme
            host = o.netloc
            if module:
                path = o.path or '/sys/version/' + module + '/'
            else:
                path = o.path or '/sys/info/'
            target = "{0}://{1}{2}".format(scheme, host, path)

            uname, password = read_credential(target)
            username = args['--username'] or uname
            password = args['--password'] or password

            # res = requests.get(target, allow_redirects=False)
            # if not username:
            #     logged_user = getpass.getuser()
            #     username = raw_input('Username: [{}] '.format(logged_user)) or logged_user
            # if not password:
            #     password = getpass.getpass()
            if username:
                res = requests.get(target, auth=(username, password))
            else:
                res = requests.get(target)

            if raw:
                stdout.write(res.content)
            else:
                res = dotdictify(res.json())
                if module:
                    stdout.write(res[module])
                elif exclude:
                    ret = dotdictify(res)
                    sections = exclude.split(',') or []
                    for sec in sections:
                        del ret[sec]
                    stdout.write(pprint.pformat(ret))
                elif only:
                    ret = {}
                    sections = only.split(',') or []
                    for sec in sections:
                        ret[sec] = getattr(res, sec)
                    stdout.write(pprint.pformat(ret))
                else:
                    stdout.write(pprint.pformat(res))
        except Exception as e:
            printout('{}: ERROR ({})'.format(param, e), RED)
        stdout.write('\n')
