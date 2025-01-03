from rest_framework import serializers
from .models import User, Patient, Medecin, Laborantin, Radiologue, Infirmier


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "password", "email", "first_name", "last_name", "user_type"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_type = instance.user_type

        if user_type == "patient" and hasattr(instance, "patient_profile"):
            patient = instance.patient_profile
            representation.update(PatientSerializer(patient).data)
            representation["patient_id"] = patient.id
        elif user_type == "medecin" and hasattr(instance, "medecin_profile"):
            medecin = instance.medecin_profile
            representation.update(MedecinSerializer(medecin).data)
            representation["medecin_id"] = medecin.id
        elif user_type == "laborantin" and hasattr(instance, "laborantin_profile"):
            laborantin = instance.laborantin_profile
            representation.update(LaborantinSerializer(laborantin).data)
            representation["laborantin_id"] = laborantin.id
        elif user_type == "radiologue" and hasattr(instance, "radiologue_profile"):
            radiologue = instance.radiologue_profile
            representation.update(RadiologueSerializer(radiologue).data)
            representation["radiologue_id"] = radiologue.id
        elif user_type == "infirmier" and hasattr(instance, "infirmier_profile"):
            infirmier = instance.infirmier_profile
            representation.update(InfirmierSerializer(infirmier).data)
            representation["infirmier_id"] = infirmier.id

        return representation


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["date_naissance", "adresse", "telephone", "NSS"]

    def create(self, validated_data):
        return Patient.objects.create(**validated_data)


class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ["date_naissance", "adresse", "telephone"]

    def create(self, validated_data):
        return Medecin.objects.create(**validated_data)


class LaborantinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laborantin
        fields = ["telephone", "department", "date_recrutement"]

    def create(self, validated_data):
        return Laborantin.objects.create(**validated_data)


class RadiologueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radiologue
        fields = ["telephone", "specialization", "date_recrutement"]

    def create(self, validated_data):
        return Radiologue.objects.create(**validated_data)
    

class InfirmierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infirmier
        # TODO: fix the fields
        fields = ["telephone", "department", "date_recrutement"]

    def create(self, validated_data):
        return Infirmier.objects.create(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(max_length=128, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)


class FakeSerializer(serializers.Serializer):
    def create(self, validated_data):
        return object()


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128, required=False)
    first_name = serializers.CharField(max_length=128, required=False)
    last_name = serializers.CharField(max_length=128, required=False)
    telephone = serializers.CharField(max_length=10, required=False)
    specialization = serializers.CharField(max_length=128, required=False)
    department = serializers.CharField(max_length=128, required=False)
    date_recrutement = serializers.DateTimeField(required=False)
    date_naissance = serializers.DateTimeField(required=False)
    adresse = serializers.CharField(max_length=128, required=False)
    NSS = serializers.CharField(max_length=50, required=False)
