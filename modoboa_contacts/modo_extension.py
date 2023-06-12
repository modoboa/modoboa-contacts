"""Declare and register the contacts extension."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool
from modoboa.parameters import tools as param_tools

from . import __version__
from . import forms


class Contacts(ModoExtension):
    """Plugin declaration."""

    name = "modoboa_contacts"
    label = gettext_lazy("Contacts")
    version = __version__
    description = gettext_lazy("Address book")
    url = "contacts"
    topredirection_url = reverse_lazy("modoboa_contacts:index")

    def load(self):
        param_tools.registry.add(
            "user", forms.UserSettings, gettext_lazy("Contacts"))


exts_pool.register_extension(Contacts)
