"""Contacts factories."""

import factory

from . import models


class EmailAddressFactory(factory.django.DjangoModelFactory):
    """Contact factory."""

    class Meta:
        model = models.EmailAddress

    type = "home"


class ContactFactory(factory.django.DjangoModelFactory):
    """Contact factory."""

    class Meta:
        model = models.Contact

    first_name = "Homer"
    last_name = "Simpson"

    @factory.post_generation
    def emails(self, create, extracted, **dummy_kwargs):
        """Add emails to contact."""
        if not create or not extracted:
            return
        for item in extracted:
            EmailAddressFactory(contact=self, address=item)
