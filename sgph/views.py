from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from users.permissions import can_get_obj

from sgph.models import Ordonnance
from sgph.serializers import OrdonnanceSerializer


@api_view(["GET"])
@permission_classes([HasAPIKey])
def get_ordonnances(request):
    """
    Allow sgph service to retrieve non validated ordonnance
    """
    ordonnances = Ordonnance.objects.filter(validated=False)
    serializer = OrdonnanceSerializer(ordonnances, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([HasAPIKey])
def get_ordonnance(request, id: int):
    """
    Allow sgph service to retrieve an ordonnance 
    """
    ordonnance = get_object_or_404(Ordonnance, id=id)
    serializer = OrdonnanceSerializer(instance=ordonnance)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([HasAPIKey])
def validate_ordonnance(request, id: int):
    """
    Allow sgph service to validate an ordonnance 
    """
    ordonnance = get_object_or_404(Ordonnance, id=id)
    ordonnance.validated = True
    ordonnance.save()

    res_serializer = OrdonnanceSerializer(instance=ordonnance)
    return Response(res_serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def consult_ordonnance(request, consultation_id):
    """
    Allow patient and Techincal team to view ordonnance
    """
    ordonnance = get_object_or_404(Ordonnance, consultation_id=consultation_id)

    if not can_get_obj(request.user, ordonnance):
        return Response(
            {"details": "You are not allowed to see data of this user"},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = OrdonnanceSerializer(instance=ordonnance)

    return Response({"ordonnance": serializer.data})
