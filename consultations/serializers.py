from rest_framework import serializers

from .models import Frais, Certificat, Resume, Consultation
from dpi_manager.models import Dpi


class FraisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frais
        fields = ["id", "date_echeance", "montant", "details"]

    def create(self, validated_data):
        consultation_id = validated_data.pop("consultation")
        frais = Frais.objects.create(**validated_data)

        consultation = Consultation.objects.get(id=consultation_id)
        consultation.frais_id = frais.id
        consultation.save()

        return frais


class CertificatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificat
        fields = ["id", "date_demande", "date_fin", "motif"]

    def create(self, validated_data):
        consultation_id = validated_data.pop("consultation")
        certificat = Certificat.objects.create(**validated_data)

        consultation = Consultation.objects.get(id=consultation_id)
        consultation.certificat_id = certificat.id
        consultation.save()

        return certificat


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "contenu", "antecedants"]

    def create(self, validated_data):
        consultation_id = validated_data.pop("consultation")
        resume = Resume.objects.create(**validated_data)

        consultation = Consultation.objects.get(id=consultation_id)
        consultation.resume_id = resume.id
        consultation.save()

        return resume


class ConsultationSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(required=False)
    frais = FraisSerializer(required=False)
    certificat = CertificatSerializer(required=False)
    dpi = serializers.PrimaryKeyRelatedField(queryset=Dpi.objects.all())

    class Meta:
        model = Consultation
        fields = ["id", "date", "resume", "frais", "certificat", "dpi"]
