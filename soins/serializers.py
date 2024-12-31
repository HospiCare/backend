from rest_framework import serializers
from .models import Soins
from consultations.models import Consultation

class SoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soins
        fields = ['id', 'date', 'soins_donnés', 'notes', 'consultation']
