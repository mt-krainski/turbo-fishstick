from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("route_summary", views.get_route_summary, name="route_summary"),
]
