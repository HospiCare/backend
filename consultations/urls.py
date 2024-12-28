from django.urls import path
from . import views

app_name = "consultation"

urlpatterns = [
    path("", views.create_consultation),
    path("<int:id>/", views.get_consultation),
    path("<int:id>/frais/create/", views.create_frais),
    path("<int:id>/frais/", views.get_frais),
    path("<int:id>/resume/create/", views.create_resume),
    path("<int:id>/resume/", views.get_resume),
    path("<int:id>/certificat/create/", views.create_certificat),
    path("<int:id>/certificat/", views.get_certificat),
]
