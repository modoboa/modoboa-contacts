"""Webmail handlers."""

from django.db.models import signals
from django.urls import reverse
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _

from modoboa.admin import models as admin_models
from modoboa.core import signals as core_signals
from modoboa.lib import signals as lib_signals

from . import models
from . import tasks


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


@receiver(core_signals.get_top_notifications)
def check_addressbook_first_sync(sender, include_all, **kwargs):
    """Check if address book first sync has been made."""
    request = lib_signals.get_request()
    qset = (
        request.user.addressbook_set.filter(last_sync__isnull=True)
    )
    if not qset.exists():
        return []
    return [{
        "id": "abook_sync_required",
        "url": reverse("modoboa_contacts:index"),
        "text": _("Your address book must be synced"),
        "level": "warning"
    }]


@receiver(signals.post_save, sender=admin_models.Mailbox)
def create_addressbook(sender, instance, created, **kwargs):
    """Create default address book for new mailbox."""
    if not created:
        return
    models.AddressBook.objects.create(
        user=instance.user, name="Contacts", _path="contacts")


@receiver(core_signals.user_login)
def sync_addressbook_with_cdav(sender, username, password, **kwargs):
    """Launch the initial address book sync if needed."""
    abook = models.AddressBook.objects.filter(
        user__username=username, last_sync__isnull=True).first()
    condition = (
        abook is None or
        not abook.user.parameters.get_value("enable_carddav_sync")
    )
    if condition:
        return
    tasks.create_cdav_addressbook(abook, password)
    if not abook.contact_set.exists():
        abook.last_sync = timezone.now()
        abook.save(update_fields=["last_sync"])


@receiver(core_signals.extra_static_content)
def inject_sync_poller(sender, caller, st_type, user, **kwargs):
    """Inject javascript code."""
    condition = (
        caller != "top" or
        st_type != "js" or
        not hasattr(user, "mailbox") or
        not user.parameters.get_value("enable_carddav_sync")
    )
    if condition:
        return ""
    return """<script>
$(document).ready(function () {
    new Poller('%s', {
        interval: %d * 1000
    });
});
</script>
""" % (reverse("api:addressbook-sync-from-cdav"),
       user.parameters.get_value("sync_frequency"))
