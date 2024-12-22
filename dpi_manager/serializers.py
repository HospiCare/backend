from rest_framework import serializers
from users.models import Patient, Medecin
from .models import Dpi
from django.contrib.auth import get_user_model


class DpiSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medecin_traitant = serializers.PrimaryKeyRelatedField(queryset=Medecin.objects.all())
    cree_par = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    qr_code = serializers.ImageField(read_only=True)

    class Meta:
        model = Dpi
        fields = [
            "id", "patient", "mutuelle", "medecin_traitant", "telephone_personne_contact", 
            "cree_par", "date_creation", "qr_code"
        ]

class DpiCreationInputSerializer(serializers.Serializer):
    nom_patient = serializers.CharField(max_length=100)
    prenom_patient = serializers.CharField(max_length=100)
    date_naissance = serializers.DateField()
    adresse_patient = serializers.CharField()
    telephone_patient = serializers.RegexField(r'^\d{10}$')
    email_patient = serializers.EmailField()
    NSS = serializers.CharField(max_length=15)
    mot_de_passe = serializers.CharField(write_only=True)
    medecin_id = serializers.IntegerField()
    mutuelle = serializers.CharField()
    telephone_personne_contact = serializers.RegexField(r'^\d{10}$')
  
