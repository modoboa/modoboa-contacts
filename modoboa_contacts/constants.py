"""Contacts constants."""

from django.utils.translation import ugettext_lazy

EMAIL_TYPES = (
    ("home", ugettext_lazy("Home")),
    ("work", ugettext_lazy("Work")),
    ("other", ugettext_lazy("Other"))
)

PHONE_TYPES = (
    ("home", ugettext_lazy("Home")),
    ("work", ugettext_lazy("Work")),
    ("other", ugettext_lazy("Other")),
    ("main", ugettext_lazy("Main")),
    ("cellular", ugettext_lazy("Cellular")),
    ("fax", ugettext_lazy("Fax")),
    ("pager", ugettext_lazy("Pager"))
)

CDAV_TO_MODEL_FIELDS_MAP = {
    "org": "company",
    "title": "position",
    "note": "note",
}
