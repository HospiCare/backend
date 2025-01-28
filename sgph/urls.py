from django.urls import path
from . import views

app_name = "sgph_api"

urlpatterns = [
    path("", views.get_ordonnances),
    path("<int:id>/", views.get_ordonnance),
    path("<int:consultation_id>/consult/", views.consult_ordonnance),
    path("<int:id>/valider", views.validate_ordonnance),
]
