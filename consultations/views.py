from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
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
from users.permissions import can_get_obj, IsMedecin


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
