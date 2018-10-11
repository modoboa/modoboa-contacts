"""Contacts views."""

from django.views import generic

from django.contrib.auth import mixins as auth_mixins


class IndexView(auth_mixins.LoginRequiredMixin, generic.TemplateView):
    """Simple view to display index page."""

    template_name = "modoboa_contacts/index.html"

    def get_context_data(self, **kwargs):
        """Set menu selection."""
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            "selection": "contacts",
            "abook_synced": self.request.user.addressbook_set.filter(
                last_sync__isnull=False).exists()
        })
        return context
