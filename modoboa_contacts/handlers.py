"""Webmail handlers."""

from django.urls import reverse
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from modoboa.core import signals as core_signals


@receiver(core_signals.extra_user_menu_entries)
def menu(sender, location, user, **kwargs):
    """Return extra menu entry."""
    if location != "top_menu" or not hasattr(user, "mailbox"):
        return []
    return [
        {"name": "contacts",
         "label": _("Contacts"),
         "url": reverse("modoboa_contacts:index")},
    ]
