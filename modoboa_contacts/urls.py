"""Contacts urls."""

from django.urls import path

from . import views

app_name = "modoboa_contacts"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index")
]
