from django.urls import path
from . import views

urlpatterns = [
    path('creer_dpi/', views.creer_dpi),  
    path('rechercher_dpi_par_NSS/', views.rechercher_dpi_par_NSS),
    path('rechercher_dpi_par_QRcode/', views.rechercher_par_QRcode),
    path('afficher_liste_dpi/', views.afficher_liste_dpi, name='afficher_liste_dpi'),

]
