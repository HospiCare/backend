from rest_framework import serializers
from .models import Ordonnance, Medicament


class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = ['id', 'name', 'dosage', 'frequency', 'duration']


class OrdonnanceSerializer(serializers.ModelSerializer):
    medicaments = MedicamentSerializer(many=True, read_only=True)

    class Meta:
        model = Ordonnance
        fields = ['id', 'validated', 'notes', 'medicaments']

