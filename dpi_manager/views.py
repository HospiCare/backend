from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Dpi
from users.models import User, Patient, Medecin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date
import json
import re


# TODO: add authorization
@csrf_exempt
def creer_dpi(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extraction des données du patient et du médecin
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

            # Vérification de la présence de toutes les données nécessaires
            if not all([nom_patient, prenom_patient, date_naissance_str, adresse_patient, telephone_patient, email_patient, NSS, mot_de_passe, medecin_id, mutuelle, telephone_personne_contact]):
                return JsonResponse({'error': 'Tous les champs sont obligatoires'}, status=400)

            # Vérification que le numéro de téléphone contient exactement 10 chiffres
            if not re.match(r'^\d{10}$', telephone_patient):
                return JsonResponse({'error': 'Le numéro de téléphone du patient doit être composé de 10 chiffres'}, status=400)
            
            if not re.match(r'^\d{10}$', telephone_personne_contact):
                return JsonResponse({'error': 'Le numéro de téléphone de la personne à contacter doit être composé de 10 chiffres'}, status=400)
           
            # Conversion de la date de naissance en format Date
            date_naissance = parse_date(date_naissance_str)
            if not date_naissance:
                return JsonResponse({'error': 'Format de la date de naissance invalide'}, status=400)

            # Recherche du médecin
            try:
                medecin = Medecin.objects.get(user__id=medecin_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Médecin non trouvé'}, status=400)

            # Création d'un nouveau utilisateur
            patient_user = User.objects.create(
                email=email_patient,
                first_name=nom_patient,
                last_name=prenom_patient,
                user_type="patient"
            )
            patient_user.set_password(mot_de_passe)
            patient_user.save()

            # Création d'un nouveau patient
            patient = Patient.objects.create(
                user=patient_user,
                date_naissance=date_naissance,
                adresse=adresse_patient,
                telephone=telephone_patient,
                NSS=NSS,
            )

            # Création du DPI
            dpi = Dpi.objects.create(
                patient=patient,
                medecin_traitant=medecin,
                mutuelle=mutuelle,
                telephone_personne_contact=telephone_personne_contact
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


def rechercher_dpi_par_NSS(request):
    
    if request.method == "GET":
        try:
            data = json.loads(request.body)
            
            NSS = data.get('NSS') 

            if not NSS:
                return JsonResponse({'error': 'Numéro de sécurité sociale est requis!!'}, status=400)

            try:
                patient = Patient.objects.get(NSS=NSS)

                dpi = Dpi.objects.get(patient=patient)

                return JsonResponse({
                    'dpi_id': dpi.id,
                    'patient': {
                        'nom': patient.user.first_name,
                        'prenom': patient.user.last_name,
                        'date_naissance': patient.date_naissance,
                        'adresse': patient.adresse,
                        'telephone': patient.telephone,
                        'email': patient.user.email,
                    },
                    'medecin_traitant': {
                        'id': dpi.medecin_traitant.user.id,
                        'nom': dpi.medecin_traitant.user.first_name,
                        'prenom': dpi.medecin_traitant.user.last_name,
                    },
                    'mutuelle': dpi.mutuelle,
                    'telephone_personne_contact': dpi.telephone_personne_contact,
                }, status=200)

            except ObjectDoesNotExist:
                return JsonResponse({'error': 'DPI non trouvé pour ce numéro de sécurité sociale'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)

    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
