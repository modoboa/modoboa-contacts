"""Contacts API urls."""

from rest_framework import routers

from . import viewsets


router = routers.SimpleRouter()
router.register(r"categories", viewsets.CategoryViewSet, base_name="category")
router.register(r"contacts", viewsets.ContactViewSet, base_name="contact")

urlpatterns = router.urls
