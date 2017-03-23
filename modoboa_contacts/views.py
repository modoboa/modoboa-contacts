"""Contacts views."""

from django.views import generic


class IndexView(generic.TemplateView):
    """Simple view to display index page."""

    template_name = "modoboa_contacts/index.html"
