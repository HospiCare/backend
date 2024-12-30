from rest_framework import serializers
from .models import BilanRadiologique, BilanBiologique,ImageMedical
from users.models import Laborantin, Radiologue
from consultations.models import Consultation
class BilanBiologiqueSerializer(serializers.ModelSerializer):
    consultation = serializers.PrimaryKeyRelatedField(queryset=Consultation.objects.all())
    laborantin = serializers.PrimaryKeyRelatedField(queryset=Laborantin.objects.all())

    class Meta:
        model = BilanBiologique
        fields = [
            "id", "consultation", "date", "laborantin", "test_type", "result", "graphique"
        ]


class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    consultation = serializers.PrimaryKeyRelatedField(queryset=Consultation.objects.all())
    radiologue = serializers.PrimaryKeyRelatedField(queryset=Radiologue.objects.all())

    class Meta:
        model = BilanRadiologique
        fields = [
            "id", "consultation", "date", "radiologue", "description"
        ]


class ImageMedicalSerializer(serializers.ModelSerializer):
    bilan_radiologique = serializers.PrimaryKeyRelatedField(queryset=BilanRadiologique.objects.all())

    class Meta:
        model = ImageMedical
        fields = [
            "id", "bilan_radiologique", "image", "uploaded_at", "notes"
        ]