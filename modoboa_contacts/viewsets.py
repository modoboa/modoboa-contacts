"""Contacts viewsets."""

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from . import models
from . import serializers


class ContactViewSet(viewsets.ModelViewSet):
    """Contact ViewSet."""

    filter_backends = [filters.SearchFilter, ]
    permission_classes = [IsAuthenticated]
    search_fields = ("^first_name", "^last_name", "^email")
    serializer_class = serializers.ContactSerializer

    def get_queryset(self):
        """Filter based on current user."""
        return models.Contact.objects.filter(user=self.request.user)
