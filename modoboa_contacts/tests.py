# coding: utf-8
"""Contacts backend tests."""

from django.core.urlresolvers import reverse

from modoboa.admin import factories as admin_factories
from modoboa.core import models as core_models
from modoboa.lib.tests import ModoAPITestCase

from . import factories
from . import models


class CategoryViewSetTestCase(ModoAPITestCase):
    """Category ViewSet tests."""

    @classmethod
    def setUpTestData(cls):
        """Create some data."""
        super(CategoryViewSetTestCase, cls).setUpTestData()
        admin_factories.populate_database()
        cls.user = core_models.User.objects.get(username="user@test.com")
        cls.category = factories.CategoryFactory(user=cls.user, name="Family")

    def test_get_categories(self):
        """Check category list endpoint."""
        url = reverse("api:category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        """Create a new category."""
        url = reverse("api:category-list")
        data = {"name": u"Amitiés"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)


class ContactViewSetTestCase(ModoAPITestCase):
    """Contact ViewSet tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        super(ContactViewSetTestCase, cls).setUpTestData()
        admin_factories.populate_database()
        cls.user = core_models.User.objects.get(username="user@test.com")
        cls.category = factories.CategoryFactory(user=cls.user, name="Family")
        cls.contact = factories.ContactFactory(
            user=cls.user, emails=["homer@simpson.com"])
        factories.ContactFactory(
            user=cls.user, first_name="Marge", emails=["marge@simpson.com"],
            categories=[cls.category]
        )
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

        response = self.client.get("{}?search=homer".format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_category(self):
        """Check filtering."""
        url = reverse("api:contact-list")
        response = self.client.get(
            "{}?category={}".format(url, self.category.name))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_contact(self):
        """Create a new contact."""
        data = {
            "first_name": "Magie", "last_name": "Simpson",
            "emails": [
                {"address": "magie@simpson.com", "type": "home"}
            ],
            "phone_numbers": [
                {"number": "+33123456789", "type": "home"}
            ]
        }
        url = reverse("api:contact-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        contact = models.Contact.objects.get(pk=response.data["pk"])
        self.assertEqual(contact.emails.first().address, "magie@simpson.com")
        self.assertEqual(
            contact.phone_numbers.first().number,
            response.data["phone_numbers"][0]["number"])

    def test_update_contact(self):
        """Update existing contact."""
        url = reverse("api:contact-detail", args=[self.contact.pk])
        data = {
            "first_name": "Homer 1", "last_name": "Simpson",
            "emails": [{"address": "duff@simpson.com", "type": "work"}],
            "phone_numbers": [
                {"number": "+33123456789", "type": "home"}
            ],
            "categories": [self.category.pk]
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        self.contact.refresh_from_db()
        self.assertEqual(self.contact.first_name, "Homer 1")
        self.assertEqual(self.contact.emails.count(), 1)
        self.assertEqual(
            self.contact.emails.first().address, "duff@simpson.com")
        self.assertEqual(self.contact.phone_numbers.count(), 1)
        self.assertEqual(self.contact.categories.first(), self.category)
