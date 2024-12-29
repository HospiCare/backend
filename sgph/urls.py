from django.urls import path
from . import views

app_name = "sgph"

urlpatterns = [
    path("create_ordonnance/", views.create_ordonnance),
    path("create_medicament/", views.create_medicament),
]