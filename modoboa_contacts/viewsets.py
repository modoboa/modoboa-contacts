"""Contacts viewsets."""

import django_filters.rest_framework
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    """Category ViewSet."""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        """Filter based on current user."""
        qset = models.Category.objects.filter(user=self.request.user)
        return qset.select_related("user")


class ContactFilter(django_filters.rest_framework.FilterSet):
    """Filter for Contact."""

    category = django_filters.CharFilter(name="categories__name")

    class Meta:
        model = models.Contact
        fields = ["categories"]


class ContactViewSet(viewsets.ModelViewSet):
    """Contact ViewSet."""

    filter_backends = [
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend]
    filter_class = ContactFilter
    permission_classes = [IsAuthenticated]
    search_fields = ("^first_name", "^last_name", "^emails__address")
    serializer_class = serializers.ContactSerializer

    def get_queryset(self):
        """Filter based on current user."""
        qset = models.Contact.objects.filter(user=self.request.user)
        return qset.select_related("user").prefetch_related(
            "categories", "emails", "phone_numbers")


class EmailAddressViewSet(viewsets.ReadOnlyModelViewSet):
    """EmailAddress viewset."""

    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    search_fields = (
        "^address", "^contact__display_name",
        "^contact__first_name", "^contact__last_name",
    )
    serializer_class = serializers.EmailAddressWithNameSerializer

    def get_queryset(self):
        """Filter based on current user."""
        return models.EmailAddress.objects.filter(
            contact__user=self.request.user)
