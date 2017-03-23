"""Contacts serializers."""

from rest_framework import serializers

from . import models


class EmailAddressSerializer(serializers.ModelSerializer):
    """Email address serializer."""

    class Meta:
        model = models.EmailAddress
        fields = ("pk", "address", "type")


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Phone number serializer."""

    class Meta:
        model = models.PhoneNumber
        fields = ("pk", "number", "type")


class ContactSerializer(serializers.ModelSerializer):
    """Contact serializer."""

    emails = EmailAddressSerializer(many=True)
    phone_numbers = PhoneNumberSerializer(many=True, required=False)

    class Meta:
        model = models.Contact
        fields = (
            "pk", "first_name", "last_name", "emails", "phone_numbers")

    def create(self, validated_data):
        """Use current user."""
        user = self.context["request"].user
        emails = validated_data.pop("emails")
        phone_numbers = validated_data.pop("phone_numbers", [])
        contact = models.Contact.objects.create(user=user, **validated_data)
        to_create = []
        for email in emails:
            to_create.append(models.EmailAddress(contact=contact, **email))
        models.EmailAddress.objects.bulk_create(to_create)
        to_create = []
        for phone_number in phone_numbers:
            to_create.append(
                models.PhoneNumber(contact=contact, **phone_number))
        if to_create:
            models.PhoneNumber.objects.bulk_create(to_create)
        return contact

    def update(self, instance, validated_data):
        """Update contact."""
        emails = validated_data.pop("emails")
        phone_numbers = validated_data.pop("phone_numbers", [])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        # Email addresses
        # FIXME: find a better way to update emails
        models.EmailAddress.objects.filter(contact=instance).delete()
        to_create = []
        for email in emails:
            to_create.append(models.EmailAddress(contact=instance, **email))
        models.EmailAddress.objects.bulk_create(to_create)
        # Phone numbers
        # FIXME: find a better way to update phones
        models.PhoneNumber.objects.filter(contact=instance).delete()
        to_create = []
        for phone_number in phone_numbers:
            to_create.append(
                models.PhoneNumber(contact=instance, **phone_number))
        if to_create:
            models.PhoneNumber.objects.bulk_create(to_create)
        return instance
