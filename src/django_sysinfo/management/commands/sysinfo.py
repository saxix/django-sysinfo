# -*- coding: utf-8 -*-
import json

from django.core.handlers.wsgi import WSGIRequest
from django.core.management.base import BaseCommand

from django_sysinfo.api import get_sysinfo


class Command(BaseCommand):
    args = ""
    help = "Help text here...."

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    #        parser.add_argument(
    #            "--database", default=DEFAULT_DB_ALIAS,
    #            help="Nominates a database to print the SQL for. Defaults to the "default" database.",
    #        )

    def handle(self, *args, **options):
        environ = {
            # "HTTP_COOKIE": self.cookies,
            "wsgi.input": "wsgi.input",
            "PATH_INFO": "/",
            "QUERY_STRING": "",
            "REQUEST_METHOD": "GET",
            "SCRIPT_NAME": "",
            "SERVER_NAME": "testserver",
            "SERVER_PORT": 80,
            "SERVER_PROTOCOL": "HTTP/1.1",
        }
        info = get_sysinfo(WSGIRequest(environ))
        print(json.dumps(info))
