from django.urls import path
from . import views

urlpatterns = [
    path('creer_dpi/', views.creer_dpi, name="creer_dpi"),  
    path('rechercher_dpi_par_NSS/', views.rechercher_dpi_par_NSS, name="rechercher_dpi_par_NSS"),
    path('rechecher_dpi_par_QRcode/', views.rechercher_par_QRcode, name="rechercher_dpi_par_QRcode")
]