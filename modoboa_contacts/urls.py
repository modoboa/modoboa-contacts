"""Contacts urls."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url("^$", views.IndexView.as_view(), name="index")
]
