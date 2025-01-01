from django.urls import path
from . import views

app_name = "soins"

urlpatterns = [
    path("remplir_soins/", views.remplir_soins),
]