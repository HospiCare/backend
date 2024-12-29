from rest_framework import serializers
from .models import Soins
from dpi_manager.models import Dpi

class SoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soins
        fields = ['id', 'date', 'soins_donnés', 'notes', 'dpi']
