"""Contacts models."""

from __future__ import unicode_literals

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from . import constants


class Category(models.Model):
    """A category for contacts."""

    user = models.ForeignKey("core.User")
    name = models.CharField(max_length=50)


class Contact(models.Model):
    """A contact."""

    user = models.ForeignKey("core.User")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    categories = models.ManyToManyField(Category, blank=True)


class EmailAddress(models.Model):
    """An email address."""

    contact = models.ForeignKey(Contact, related_name="emails")
    address = models.EmailField()
    type = models.CharField(
        max_length=20, choices=constants.EMAIL_TYPES)


class PhoneNumber(models.Model):
    """A phone number."""

    contact = models.ForeignKey(Contact, related_name="phone_numbers")
    number = PhoneNumberField()
    type = models.CharField(
        max_length=20, choices=constants.PHONE_TYPES)
