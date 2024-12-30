from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Dpi
from users.models import Patient,Medecin
from .serializers import DpiSerializer, DpiCreationInputSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound
from PIL import Image
from pyzbar.pyzbar import decode
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsMedecin

@csrf_exempt
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
def creer_dpi(request):
    try:

        data = request.data
        serializer = DpiCreationInputSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        nom_patient = data.get('nom_patient')
        prenom_patient = data.get('prenom_patient')
        date_naissance_str = data.get('date_naissance')
        adresse_patient = data.get('adresse_patient')
        telephone_patient = data.get('telephone_patient')
        email_patient = data.get('email_patient')
        NSS = data.get('NSS')
        mot_de_passe = data.get('mot_de_passe')
        medecin_id = data.get('medecin_id')
        mutuelle = data.get('mutuelle')
        telephone_personne_contact = data.get('telephone_personne_contact')

        try:
            medecin = Medecin.objects.get(id=medecin_id)
        except Medecin.DoesNotExist:
            return Response({'error': f'Médecin avec ID {medecin_id} introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        user = get_user_model().objects.create_user(
            email=email_patient,
            password=mot_de_passe,
            first_name=nom_patient,
            last_name=prenom_patient,
            user_type='patient'
        )

        patient = Patient.objects.create(
            user=user,
            date_naissance=date_naissance_str,
            adresse=adresse_patient,
            telephone=telephone_patient,
            NSS=NSS
        )

        if request.user.user_type == 'medecin':
            cree_par_value = f"Médecin : {request.user.get_full_name()}"
        elif request.user.is_superuser or request.user.user_type == 'admin':
            cree_par_value = f"Admin : {request.user.get_full_name()}"
        else:
            return Response(
                {"error": "Seuls un médecin ou un administrateur peuvent créer un DPI."},
                status=status.HTTP_403_FORBIDDEN
            )
        dpi = Dpi.objects.create(
            patient=patient,
            medecin_traitant=medecin,
            mutuelle=mutuelle,
            telephone_personne_contact=telephone_personne_contact,
            cree_par=cree_par_value  
        )

        dpi_serializer = DpiSerializer(dpi)
        return Response({'success': 'DPI créé avec succès', 'dpi': dpi_serializer.data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Erreur : {str(e)}")
        return Response({'error': f'Erreur interne : {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def rechercher_dpi_par_NSS(request):
    NSS = request.query_params.get("NSS")  
    if not NSS:
        return Response({'error': 'Numéro de sécurité sociale est requis!'}, status=400)

    try:
        patient = Patient.objects.get(NSS=NSS)
        dpi = Dpi.objects.get(patient=patient)
        
        serializer = DpiSerializer(dpi)

        response_data = serializer.data
        response_data['patient_details'] = {
            'nom': patient.user.first_name,
            'prenom': patient.user.last_name,
            'date_naissance': patient.date_naissance,
            'adresse': patient.adresse,
            'telephone': patient.telephone,
            'email': patient.user.email,
        }
        if dpi.medecin_traitant:
            response_data['medecin_traitant_details'] = {
                'nom': dpi.medecin_traitant.user.first_name,
                'prenom': dpi.medecin_traitant.user.last_name,
            }
        else:
            response_data['medecin_traitant_details'] = None

        return Response(response_data, status=200)

    except Patient.DoesNotExist:
        raise NotFound('Patient non trouvé avec ce NSS.')
    except Dpi.DoesNotExist:
        raise NotFound('DPI non trouvé pour ce patient.')
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def rechercher_par_QRcode(request):
    try:
        if 'qr_code' not in request.FILES:
            return Response({'error': 'Aucune image de QR code fournie'}, status=400)
        
        qr_image = request.FILES['qr_code']
        
        image = Image.open(qr_image)
        qr_data = decode(image)
        
        if not qr_data:
            return Response({'error': 'QR code invalide ou non détecté'}, status=400)
        
        # Le QR code devrait contenir le NSS sous cette forme: 'NSS:le numéro de sécurité sociale du patient'
        decoded_data = qr_data[0].data.decode('utf-8')
        if not decoded_data.startswith("NSS:"):
            return Response({'error': 'QR code invalide, le format NSS attendu est manquant'}, status=400)
        
        nss = decoded_data.split("NSS:")[1].strip()

        try:
            patient = Patient.objects.get(NSS=nss)
            dpi = Dpi.objects.get(patient=patient)
            serializer = DpiSerializer(dpi)

        except Patient.DoesNotExist:
            return Response({'error': 'Patient non trouvé avec ce NSS'}, status=404)
        except Dpi.DoesNotExist:
            return Response({'error': 'DPI non trouvé pour ce patient'}, status=404)
        
        response_data = serializer.data
        response_data = {
            'success': 'DPI trouvé',
            'dpi_id': dpi.id,
            'patient_details': {
                'nom': patient.user.first_name,
                'prenom': patient.user.last_name,
                'date_naissance': patient.date_naissance,
                'adresse': patient.adresse,
                'telephone': patient.telephone,
                'email': patient.user.email,
            },
            'medecin_traitant_details': {
                'nom': dpi.medecin_traitant.user.first_name if dpi.medecin_traitant else None,
                'prenom': dpi.medecin_traitant.user.last_name if dpi.medecin_traitant else None,
            },
            'mutuelle': dpi.mutuelle,
            'telephone_personne_contact': dpi.telephone_personne_contact,
        }
        return Response(response_data, status=200)

    except Exception as e:
        return Response({'error': f'Erreur serveur: {str(e)}'}, status=500)