"""Contacts models."""

from __future__ import unicode_literals

from django.db import models

from . import constants


class Category(models.Model):
    """A category for contacts."""

    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Contact(models.Model):
    """A contact."""

    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    display_name = models.CharField(max_length=60, blank=True)
    birth_date = models.DateField(null=True)

    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=200, blank=True)

    address = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    note = models.TextField(blank=True)

    categories = models.ManyToManyField(Category, blank=True)


class EmailAddress(models.Model):
    """An email address."""

    contact = models.ForeignKey(Contact, related_name="emails",
                                on_delete=models.CASCADE)
    address = models.EmailField()
    type = models.CharField(
        max_length=20, choices=constants.EMAIL_TYPES)


class PhoneNumber(models.Model):
    """A phone number."""

    contact = models.ForeignKey(Contact, related_name="phone_numbers",
                                on_delete=models.CASCADE)
    number = models.CharField(max_length=40)
    type = models.CharField(
        max_length=20, choices=constants.PHONE_TYPES)
