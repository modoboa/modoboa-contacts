"""Contacts viewsets."""

import django_filters.rest_framework
from rest_framework import decorators, filters, response, viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers
from . import tasks


class AddressBookViewSet(viewsets.GenericViewSet):
    """Address book viewset."""

    permission_classes = (IsAuthenticated, )

    @decorators.list_route(methods=["get"])
    def default(self, request, *args, **kwargs):
        """Return default user address book."""
        abook = request.user.addressbook_set.first()
        if not abook:
            return response.Response(status_code=404)
        serializer = serializers.AddressBookSerializer(abook)
        return response.Response(serializer.data)

    @decorators.list_route(methods=["get"])
    def sync_to_cdav(self, request, *args, **kwargs):
        """Synchronize address book with CardDAV collection."""
        abook = request.user.addressbook_set.first()
        if request.user.parameters.get_value("enable_carddav_sync"):
            tasks.push_addressbook_to_carddav(request, abook)
        return response.Response({})

    @decorators.list_route(methods=["get"])
    def sync_from_cdav(self, request, *args, **kwargs):
        """Synchronize from CardDAV address book."""
        abook = request.user.addressbook_set.first()
        if not abook.last_sync:
            return response.Response()
        if request.user.parameters.get_value("enable_carddav_sync"):
            tasks.sync_addressbook_from_cdav(request, abook)
        return response.Response({})


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
        qset = models.Contact.objects.filter(
            addressbook__user=self.request.user)
        return qset.prefetch_related(
            "categories", "emails", "phone_numbers")

    def perform_destroy(self, instance):
        """Also remove cdav contact."""
        if self.request.user.parameters.get_value("enable_carddav_sync"):
            tasks.delete_contact_cdav(self.request, instance)
        instance.delete()


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
            contact__addressbook__user=self.request.user)
