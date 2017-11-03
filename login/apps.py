# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class LoginConfig(AppConfig):
    name = 'login'

    def ready(self):
        from . import signals