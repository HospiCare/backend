from rest_framework import serializers
from .models import Frais, Certificat, Resume, Consultation
from dpi_manager.models import Dpi


class FraisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frais
        fields = ['id', 'date_echeance', 'montant', 'details'] 


class CertificatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificat
        fields = ['id', 'date_demande', 'date_fin', 'motif']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'contenu', 'antecedants']


class ConsultationSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(required=False)  
    frais = FraisSerializer(required=False)
    certificat = CertificatSerializer(required=False)
    dpi = serializers.PrimaryKeyRelatedField(queryset=Dpi.objects.all())

    class Meta:
        model = Consultation
        fields = ['id', 'date', 'resume', 'frais', 'certificat', 'dpi']

