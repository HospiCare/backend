
from users.permissions import can_get_obj, IsInfirmier
from .serializers import SoinsSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import Infirmier
from soins.models import Soins
from consultations.models import Consultation
from django.shortcuts import get_object_or_404


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsInfirmier])
def remplir_soins(request):
    try:
        data = request.data
        
        consultation_id = data.get('consultation')
        try:
            consultation = Consultation.objects.get(id=consultation_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Consultation non trouvée.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            infirmier = Infirmier.objects.get(user=request.user)
        except Infirmier.DoesNotExist:
            return Response({'error': 'Infirmier non trouvé.'}, status=status.HTTP_400_BAD_REQUEST)
        
        soins_data = {
            'soins_donnés': data.get('soins_donnés', ''),
            'notes': data.get('notes', ''),
            'consultation': consultation.id,
            'infirmier': infirmier.id,  
        }

        soins_serializer = SoinsSerializer(data=soins_data)
        if soins_serializer.is_valid():
            soins = soins_serializer.save()
            return Response({'success': 'Soins créés avec succès.', 'soins': soins_serializer.data}, status=status.HTTP_201_CREATED)

        return Response(soins_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return Response({'error': f'Erreur interne du serveur : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def afficher_liste_soins(request):
    try:
        user = request.user
        soins = None
        data = []

        if IsInfirmier().has_permission(request, None):
            try:
                infirmier = Infirmier.objects.get(user=user)
            except Infirmier.DoesNotExist:
                return Response({"error": "Infirmier non trouvé."}, status=status.HTTP_404_NOT_FOUND)

            soins = Soins.objects.filter(infirmier=infirmier).order_by('-consultation__date')

        else:
            return Response({"error": "Utilisateur non autorisé à afficher les soins."}, status=status.HTTP_403_FORBIDDEN)

        for soin in soins:
            consultation = soin.consultation
            patient = consultation.dpi.patient
            medecin = consultation.dpi.medecin_traitant
            data.append({
                'id_soin': soin.id,
                'date': soin.date,
                'soins_donnes': soin.soins_donnés,
                'notes': soin.notes,
                'consultation': {
                    'id': consultation.id,
                    'date_creation': consultation.date,
                },
                'patient': {
                    'id': patient.user.id,
                    'nom': patient.user.first_name,
                    'prenom': patient.user.last_name,
                },
                'medecin': {
                    'email': medecin.user.email,
                } if medecin else None,
            })

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Erreur lors de la récupération des soins : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_soin(request, id):
    try:
        soin = get_object_or_404(Soins, id=id)
    except Soins.DoesNotExist:
        return Response({"detail": "Soin non trouvé."}, status=status.HTTP_404_NOT_FOUND)

    if not can_get_obj(request.user, soin):
        return Response(
            {"detail": "Vous n'êtes pas autorisé à consulter ce soin."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = SoinsSerializer(soin)
    return Response(serializer.data, status=status.HTTP_200_OK)
