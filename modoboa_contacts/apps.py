from __future__ import unicode_literals

from django.apps import AppConfig


class ModoboaContactsConfig(AppConfig):
    name = "modoboa_contacts"

    def ready(self):
        from . import handlers
