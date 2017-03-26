"""Contacts backend tests."""

from django.core.urlresolvers import reverse

from modoboa.admin import factories as admin_factories
from modoboa.core import models as core_models
from modoboa.lib.tests import ModoAPITestCase

from . import factories


class ContactViewSetTestCase(ModoAPITestCase):
    """Contact ViewSet tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        super(ContactViewSetTestCase, cls).setUpTestData()
        admin_factories.populate_database()
        cls.user = core_models.User.objects.get(username="user@test.com")
        factories.ContactFactory(user=cls.user, emails=["homer@simpson.com"])
        factories.ContactFactory(
            user=cls.user, first_name="Marge", emails=["marge@simpson.com"])
        factories.ContactFactory(
            user=cls.user, first_name="Bart", emails=["bart@simpson.com"])

    def setUp(self):
        """Initiate test context."""
        self.client.force_login(self.user)

    def test_contact_list(self):
        """Check contact list endpoint."""
        url = reverse("api:contact-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
