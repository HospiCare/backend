from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from users.permissions import can_get_obj, IsMedecin

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from consultations.models import Consultation, Frais, Resume, Certificat
from consultations.serializers import (
    ConsultationSerializer,
    FraisSerializer,
    ResumeSerializer,
    CertificatSerializer,
)
from sgph.serializers import OrdonnanceSerializer, MedicamentSerializer
from sgph.models import Ordonnance, Medicament
from django.shortcuts import get_object_or_404
from users.models import Medecin, Patient

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsMedecin])
def create_consultation(request):
    """
    Allow medecin to create consultation
    """
    serializer = ConsultationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    consultation = Consultation.objects.create(**serializer.validated_data)
    res_serializer = ConsultationSerializer(instance=consultation)
    return Response({"consultation": res_serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_consultation(request, id):
    """
    Allow patient and Techincal team to view consultation
    """
    consultation = get_object_or_404(Consultation, id=id)

    if not can_get_obj(request.user, consultation):
        return Response(
            {"details": "You are not allowed to see data of this user"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = ConsultationSerializer(instance=consultation)

    return Response({"consultation": serializer.data})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsMedecin])
def create_frais(request, id):
    serializer = FraisSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.validated_data["consultation"] = id
    frais = FraisSerializer().create(serializer.validated_data)

    res_serializer = FraisSerializer(instance=frais)
    return Response({"frais": res_serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_frais(request, id):
    frais = get_object_or_404(Frais, consultation=id)
    if not can_get_obj(request.user, frais):
        return Response(
            {"details": "You are not allowed to see data of this user"},
            status=status.HTTP_403_FORBIDDEN,
        )

    res_serializer = FraisSerializer(instance=frais)
    return Response({"frais": res_serializer.data})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsMedecin])
def create_resume(request, id):
    serializer = ResumeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.validated_data["consultation"] = id
    resume = ResumeSerializer().create(serializer.validated_data)

    res_serializer = ResumeSerializer(instance=resume)
    return Response({"resume": res_serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_resume(request, id):
    resume = get_object_or_404(Resume, consultation=id)
    if not can_get_obj(request.user, resume):
        return Response(
            {"details": "You are not allowed to see data of this user"},
            status=status.HTTP_403_FORBIDDEN,
        )

    res_serializer = ResumeSerializer(instance=resume)
    return Response({"resume": res_serializer.data})


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsMedecin])
def create_certificat(request, id):
    serializer = CertificatSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.validated_data["consultation"] = id
    certificat = CertificatSerializer().create(serializer.validated_data)

    res_serializer = CertificatSerializer(instance=certificat)
    return Response({"certificat": res_serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_certificat(request, id):
    certificat = get_object_or_404(Certificat, consultation=id)
    if not can_get_obj(request.user, certificat):
        return Response(
            {"details": "You are not allowed to see data of this user"},
            status=status.HTTP_403_FORBIDDEN,
        )

    res_serializer = CertificatSerializer(instance=certificat)

    return Response({"certificat": res_serializer.data})





@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsMedecin])
def creer_ordonnance(request, consultation_id):
    try:
        consultation = Consultation.objects.get(id=consultation_id)

        if hasattr(consultation, 'ordonnance'):
            return Response(
                {"error": "Une ordonnance existe déjà pour cette consultation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ordonnance_data = request.data.get('ordonnance', {})
        notes = ordonnance_data.get('notes', '')

        ordonnance = Ordonnance.objects.create(
            consultation=consultation,
            notes=notes
        )

        medicaments_data = request.data.get('medicaments', [])
        for medicament_data in medicaments_data:
            Medicament.objects.create(
                ordonnance=ordonnance,
                name=medicament_data['name'],
                dosage=medicament_data['dosage'],
                frequency=medicament_data['frequency'],
                duration=medicament_data['duration']
            )

        return Response(
            {"success": "Ordonnance créée avec succès"},
            status=status.HTTP_201_CREATED
        )

    except Consultation.DoesNotExist:
        return Response(
            {"error": "Consultation introuvable."},
            status=status.HTTP_404_NOT_FOUND
        )
    except KeyError as e:
        return Response(
            {"error": f"Champ manquant: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": f"Erreur interne: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])

def get_ordonnance(request, ordonnance_id):
    try:
        ordonnance = Ordonnance.objects.prefetch_related('medicaments').get(id=ordonnance_id)

        if not can_get_obj(request.user, ordonnance):
            return Response({"error": "Permission refusée."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrdonnanceSerializer(ordonnance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Ordonnance.DoesNotExist:
        return Response({"error": "Ordonnance introuvable."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Erreur interne : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def afficher_consultations(request, patientId):
    try:
        user = request.user
        data = []

        # Cas : Médecin
        if IsMedecin().has_permission(request, None):
            try:
                medecin = Medecin.objects.get(user=user)
            except Medecin.DoesNotExist:
                return Response({"error": "Médecin non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            if not patientId:
                return Response({"error": "ID du patient manquant."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                patient = Patient.objects.get(id=patientId)
            except Patient.DoesNotExist:
                return Response({"error": "Patient non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            consultations = Consultation.objects.filter(
                dpi__patient=patient, dpi__medecin_traitant=medecin
            ).order_by('-date')

        # Cas : Patient
        else:
            try:
                patient = Patient.objects.get(user=user)
            except Patient.DoesNotExist:
                return Response({"error": "Patient non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            consultations = Consultation.objects.filter(dpi__patient=patient).order_by('-date')

        for consultation in consultations:
            medecin = consultation.dpi.medecin_traitant
            data.append({
                'id': consultation.id,
                'date': consultation.date.strftime('%Y-%m-%d %H:%M:%S'),
                'medecin': {
                    'id': medecin.user.id,
                    'name': f"{medecin.user.first_name} {medecin.user.last_name}",
                    'email': medecin.user.email,
                }
            })

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Erreur lors de la récupération des consultations : {str(e)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
