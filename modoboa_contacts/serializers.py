"""Contacts serializers."""

from django.utils.translation import ugettext as _

from rest_framework import serializers

from . import models


class EmailAddressSerializer(serializers.ModelSerializer):
    """Email address serializer."""

    class Meta:
        model = models.EmailAddress
        fields = ("pk", "address", "type")


class EmailAddressWithNameSerializer(serializers.ModelSerializer):
    """Email address + contact name serializer."""

    display_name = serializers.SerializerMethodField()

    class Meta:
        model = models.EmailAddress
        fields = ("pk", "address", "type", "display_name")

    def get_display_name(self, obj):
        """Return display name."""
        if obj.contact.display_name:
            return obj.contact.display_name
        return u"{} {}".format(obj.contact.first_name, obj.contact.last_name)


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Phone number serializer."""

    class Meta:
        model = models.PhoneNumber
        fields = ("pk", "number", "type")


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""

    class Meta:
        model = models.Category
        fields = ("pk", "name")

    def create(self, validated_data):
        """Use current user."""
        user = self.context["request"].user
        return models.Category.objects.create(user=user, **validated_data)


class ContactSerializer(serializers.ModelSerializer):
    """Contact serializer."""

    emails = EmailAddressSerializer(many=True)
    phone_numbers = PhoneNumberSerializer(many=True, required=False)

    class Meta:
        model = models.Contact
        fields = (
            "pk", "first_name", "last_name", "categories", "emails",
            "phone_numbers", "company", "position",
            "address", "zipcode", "city", "country", "state",
            "note", "birth_date", "display_name"
        )

    def validate(self, data):
        """Make sure display name or first/last names are set."""
        condition = (
            "first_name" not in data and
            "last_name" not in data and
            "display_name" not in data
        )
        if condition:
            msg = _("Name or display name required")
            raise serializers.ValidationError({
                "first_name": msg,
                "last_name": msg,
                "display_name": msg
            })
        return data

    def create(self, validated_data):
        """Use current user."""
        user = self.context["request"].user
        categories = validated_data.pop("categories", [])
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
        if categories:
            qset = models.Categories.objects.filter(pk__in=categories)
            for category in qset:
                contact.categories.add(category)
        return contact

    def update(self, instance, validated_data):
        """Update contact."""
        emails = validated_data.pop("emails")
        phone_numbers = validated_data.pop("phone_numbers", [])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        addresses = dict(
            (address.pk, address)
            for address in instance.emails.all())
        to_create = []
        for email in emails:
            pk = email.get("pk")
            if not pk:
                to_create.append(
                    models.EmailAddress(contact=instance, **email))
                continue
            condition = (
                addresses[pk].type != email["type"] or
                addresses[pk].address != email["address"])
            if condition:
                addresses[pk].type = email["type"]
                addresses[pk].address = email["address"]
                addresses[pk].save()
            del addresses[pk]
        models.EmailAddress.objects.filter(pk__in=addresses.keys()).delete()
        models.EmailAddress.objects.bulk_create(to_create)

        phones = dict(
            (phone.pk, phone)
            for phone in instance.phone_numbers.all())
        to_create = []
        for phone in phone_numbers:
            pk = phone.get("pk")
            if not pk:
                to_create.append(
                    models.PhoneNumber(contact=instance, **phone))
                continue
            condition = (
                phones[pk].type != phone["type"] or
                phones[pk].number != phone["number"])
            if condition:
                phones[pk].type = phone["type"]
                phones[pk].number = phone["number"]
                phones[pk].save()
            del phones[pk]
        models.PhoneNumber.objects.filter(pk__in=phones.keys()).delete()
        models.PhoneNumber.objects.bulk_create(to_create)

        return instance
