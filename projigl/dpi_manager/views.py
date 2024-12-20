from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Dpi, Patient, Medecin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
import json


@csrf_exempt  
def creer_dpi(request):
    print("debut")
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extraction des données du patient et du médecin
            nom_patient = data.get('nom_patient')
            prenom_patient = data.get('prenom_patient')
            date_naissance_str = data.get('date_naissance')
            medecin_id = data.get('medecin_id')
            print(request.body)
            # Vérification de la présence de toutes les données nécessaires
            if not all([nom_patient, prenom_patient, date_naissance_str, medecin_id]):
                return JsonResponse({'error': 'Tous les champs sont obligatoires'}, status=400)


            # Conversion de la date de naissance en format Date
            date_naissance = parse_date(date_naissance_str)
            if not date_naissance:
                return JsonResponse({'error': 'Format de la date de naissance invalide'}, status=400)


            # Création d'un nouveau patient
            patient = Patient.objects.create(
                nom=nom_patient,
                prenom=prenom_patient,
                date_naissance=date_naissance
            )


            # Recherche du médecin
            try:
                medecin = Medecin.objects.get(id=medecin_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Médecin non trouvé'}, status=400)


            # Création du DPI
            dpi = Dpi.objects.create(
                patient=patient,
                medecin_traitant=medecin,
            )


            return JsonResponse({'success': 'DPI créé avec succès', 'dpi_id': dpi.id}, status=201)


        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Erreur serveur: {str(e)}'}, status=500)


    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)



