from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("", views.create_account),
    path("change_password/", views.change_password),
    path("<int:id>/", views.get_profile),
]
