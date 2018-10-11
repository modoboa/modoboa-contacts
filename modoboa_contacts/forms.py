"""Contacts forms."""

from django.utils.translation import ugettext_lazy as _

from modoboa.lib import form_utils
from modoboa.parameters import forms as param_forms


class UserSettings(param_forms.UserParametersForm):
    """User settings."""

    app = "modoboa_contacts"

    sep1 = form_utils.SeparatorField(label=_("Synchronization"))

    enable_carddav_sync = form_utils.YesNoField(
        initial=False,
        label=_("Synchonize address book using CardDAV"),
        help_text=_(
            "Choose to synchronize or not your address book using CardDAV. "
            "You will be able to access your contacts from the outside."
        )
    )
