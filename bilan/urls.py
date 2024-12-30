from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/generer_graphe_simple/', views.generer_graphe_simple), 
    path('<int:nouveau_bilan_id>/generer_graphe_empile/', views.generer_graphe_empile),
    path('creer_bilan_biologique/', views.creer_bilan_biologique),  
    path('creer_bilan_radiologique/', views.creer_bilan_radiologique),  
    path('ajouter_image_medicale/', views.ajouter_image_medicale),
    path('<int:id>/remplir_bilan_biologique/', views.remplir_bilan_biologique),
    path('afficher_liste_bilans/', views.afficher_liste_bilans),
    path('<int:id>/get_bilan_biologique/', views.get_bilan_biologique),
    path('<int:id>/get_bilan_radiologique/', views.get_bilan_radiologique),

]