# coding: utf-8
"""Contacts backend tests."""

from django.urls import reverse

from modoboa.admin import factories as admin_factories
from modoboa.core import models as core_models
from modoboa.lib.tests import ModoAPITestCase, ModoTestCase

from . import factories
from . import models


class TestDataMixin(object):
    """Create some data."""

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        super(TestDataMixin, cls).setUpTestData()
        admin_factories.populate_database()
        cls.user = core_models.User.objects.get(username="user@test.com")
        cls.category = factories.CategoryFactory(user=cls.user, name="Family")
        cls.contact = factories.ContactFactory(
            user=cls.user, emails=["homer@simpson.com"],
            phone_numbers=["01234567889"],
        )
        factories.ContactFactory(
            user=cls.user, first_name="Marge", emails=["marge@simpson.com"],
            categories=[cls.category]
        )
        factories.ContactFactory(
            user=cls.user, first_name="Bart", emails=["bart@simpson.com"])


class ViewsTestCase(TestDataMixin, ModoTestCase):
    """Check views."""

    def setUp(self):
        """Initiate test context."""
        self.client.force_login(self.user)

    def test_index(self):
        """Test index view."""
        url = reverse("modoboa_contacts:index")
        response = self.client.get(url)
        self.assertContains(response, '<div id="app">')


class CategoryViewSetTestCase(TestDataMixin, ModoAPITestCase):
    """Category ViewSet tests."""

    def setUp(self):
        """Initiate test context."""
        self.client.force_login(self.user)

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

    def test_update_category(self):
        """Update a category."""
        url = reverse("api:category-detail", args=[self.category.pk])
        data = {"name": u"Test"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Test")

    def test_delete_category(self):
        """Try to delete a category."""
        url = reverse("api:category-detail", args=[self.category.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(models.Category.DoesNotExist):
            self.category.refresh_from_db()


class ContactViewSetTestCase(TestDataMixin, ModoAPITestCase):
    """Contact ViewSet tests."""

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
        self.assertEqual(contact.display_name, "Magie Simpson")

    def test_create_contact_quick(self):
        """Create a contact with minimal information."""
        data = {
            "emails": [
                {"address": "magie@simpson.com", "type": "home"}
            ]
        }
        url = reverse("api:contact-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["display_name"][0],
                         "Name or display name required")

        data["display_name"] = "Magie Simpson"
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_contact_with_category(self):
        """Create a new contact with a category."""
        data = {
            "first_name": "Magie", "last_name": "Simpson",
            "emails": [
                {"address": "magie@simpson.com", "type": "home"}
            ],
            "categories": [self.category.pk]
        }
        url = reverse("api:contact-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        contact = models.Contact.objects.get(pk=response.data["pk"])
        self.assertEqual(contact.categories.first(), self.category)

    def test_update_contact(self):
        """Update existing contact."""
        url = reverse("api:contact-detail", args=[self.contact.pk])
        email_pk = self.contact.emails.first().pk
        data = {
            "first_name": "Homer 1", "last_name": "Simpson",
            "emails": [
                {"address": "duff@simpson.com", "type": "work"},
                {"address": "homer@simpson.com", "type": "other"}
            ],
            "phone_numbers": [
                {"number": "+33123456789", "type": "home"},
                {"number": "01234567889", "type": "work"},
            ],
            "categories": [self.category.pk]
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)

        self.contact.refresh_from_db()
        self.assertEqual(self.contact.first_name, "Homer 1")
        self.assertEqual(self.contact.emails.count(), 2)
        self.assertEqual(
            models.EmailAddress.objects.get(pk=email_pk).type, "other")
        self.assertEqual(self.contact.phone_numbers.count(), 2)
        self.assertEqual(self.contact.categories.first(), self.category)

        data["emails"].pop(1)
        data["phone_numbers"].pop(1)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.contact.emails.count(), 1)
        self.assertEqual(self.contact.phone_numbers.count(), 1)

    def test_delete_contact(self):
        """Try to delete a contact."""
        url = reverse("api:contact-detail", args=[self.contact.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(models.Contact.DoesNotExist):
            self.contact.refresh_from_db()


class EmailAddressViewSetTestCase(TestDataMixin, ModoAPITestCase):
    """EmailAddressViewSet tests."""

    def setUp(self):
        """Initiate test context."""
        self.client.force_login(self.user)

    def test_emails_list(self):
        """Check list endpoint."""
        url = reverse("api:emailaddress-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        response = self.client.get("{}?search=homer".format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get("{}?search=Marge".format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = self.client.get("{}?search=Simpson".format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
