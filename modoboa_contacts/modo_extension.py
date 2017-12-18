"""Declare and register the contacts extension."""

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool

from . import __version__


class Contacts(ModoExtension):
    """Plugin declaration."""

    name = "modoboa_contacts"
    label = ugettext_lazy("Contacts")
    version = __version__
    description = ugettext_lazy("Address book")
    url = "contacts"
    topredirection_url = reverse_lazy("modoboa_contacts:index")

    def load(self):
        pass


exts_pool.register_extension(Contacts)
