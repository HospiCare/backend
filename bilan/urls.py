from django.urls import path
from . import views

urlpatterns = [
    path('creer_bilan_biologique/', views.creer_bilan_biologique),  
    path('creer_bilan_radiologique/', views.creer_bilan_radiologique),  
    path('ajouter_image_medicale/', views.ajouter_image_medicale),
    path('<int:id>/update_bilan_biologique/', views.update_bilan_biologique),
]
