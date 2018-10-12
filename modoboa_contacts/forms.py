"""Contacts forms."""

from django import forms
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

    sync_frequency = forms.IntegerField(
        initial=300,
        label=_("Synchronization frequency"),
        help_text=_(
            "Interval in seconds between 2 synchronization requests"
        )
    )

    visibility_rules = {
        "sync_frequency": "enable_carddav_sync=True"
    }

    def clean_sync_frequency(self):
        """Make sure frequency is a positive integer."""
        if self.cleaned_data["sync_frequency"] < 60:
            raise forms.ValidationError(
                _("Minimum allowed value is 60s")
            )
        return self.cleaned_data["sync_frequency"]
