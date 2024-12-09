from django.urls import path
from . import views

urlpatterns = [
    path('', views.fake_endpoint, name="fake_endpoint"),
]
