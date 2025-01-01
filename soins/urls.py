from django.urls import path
from . import views

app_name = "soins"

urlpatterns = [
    path("remplir_soins/", views.remplir_soins),
    path('afficher_liste_soins/', views.afficher_liste_soins),
    path('<int:id>/get_soin/', views.get_soin),

]