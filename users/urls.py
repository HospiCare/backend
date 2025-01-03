from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("", views.create_account),
    path("change_password/", views.change_password),
    path("<int:id>/update/", views.change_profile),
    path("<int:id>/", views.get_user),
    path("medecins/", views.get_list_medecins),
    path("rechercher_patients/", views.rechercher_patients),
    path("rechercher_laborantins/", views.rechercher_laborantins),
    path("rechercher_radiologues/", views.rechercher_radiologues),
    path("rechercher_infirmiers/", views.rechercher_infirmiers),

]
