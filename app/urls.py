"""
URL configuration for projigl project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('docs/', include('docs.urls')),
    path('admin/', admin.site.urls),
    path('dpi_manager/', include('dpi_manager.urls')),  
    path('user/', include('users.urls')),
    path('bilan/', include('bilan.urls')),
    path('consultation/', include('consultations.urls')),
    path('soins/', include('soins.urls')),
    path('sgph/', include('sgph.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
