from django.urls import path
from . import views

urlpatterns = [
    path('creer_dpi/', views.creer_dpi, name="creer_dpi"),  

]