"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('docs/', include('docs.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls'))
]
