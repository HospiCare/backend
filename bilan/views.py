import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.conf import settings
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import *
from . serializers import *
from django.shortcuts import get_object_or_404

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsMedecin])
def creer_bilan_biologique(request):
    try:
        data = request.data
        serializer = BilanBiologiqueSerializer(data=data, partial=True)  # Allow partial input
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        consultation_id = data.get("consultation")
        laborantin_id = data.get("laborantin")
        test_type = data.get("test_type")

        # Ensure required relationships exist
        try:
            consultation = Consultation.objects.get(id=consultation_id)
        except Consultation.DoesNotExist:
            return Response({"error": "Consultation introuvable"}, status=status.HTTP_404_NOT_FOUND)

        try:
            laborantin = Laborantin.objects.get(id=laborantin_id)
        except Laborantin.DoesNotExist:
            return Response({"error": "Laborantin introuvable"}, status=status.HTTP_404_NOT_FOUND)

        # Create BilanBiologique without result and graphique
        bilan_biologique = BilanBiologique.objects.create(
            consultation=consultation,
            laborantin=laborantin,
            test_type=test_type,
            result=None,  # Ensure result is empty
            graphique=None  # Ensure graphique is empty
        )

        response_serializer = BilanBiologiqueSerializer(bilan_biologique)
        return Response({"success": "Bilan biologique créé avec succès", "bilan": response_serializer.data},
                        status=status.HTTP_201_CREATED)

    except Exception as e:
 
       return Response({"error": f"Erreur interne : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsLaborantin])
def remplir_bilan_biologique(request, id):
    try:
        data = request.data
        bilan_biologique = BilanBiologique.objects.get(id=id)

        allowed_fields = {"result", "graphique"}
        update_data = {key: data[key] for key in data if key in allowed_fields}

        if "result" in update_data:
            result_data = update_data["result"]
            expected_tests = {"test1", "test2", "test3", "test4"}
            if not all(test in expected_tests for test in result_data.keys()):
                return Response({"error": "Tests invalides dans le résultat"}, status=status.HTTP_400_BAD_REQUEST)

        for field, value in update_data.items():
            setattr(bilan_biologique, field, value)

        bilan_biologique.save()

        patient_id = bilan_biologique.consultation.dpi.patient.id
        type_bilan = bilan_biologique.test_type

        bilan_anterieur = BilanBiologique.objects.filter(
            consultation__dpi__patient_id=patient_id,
            test_type=type_bilan,
            id__lt=bilan_biologique.id
        ).order_by('-id').first()

        if bilan_anterieur:
            try:
                result_nouveau = bilan_biologique.result
                result_ancien = bilan_anterieur.result
                if isinstance(result_nouveau, dict) and isinstance(result_ancien, dict):
                    image_url = generer_graphe_empile(result_ancien, result_nouveau, patient_id, bilan_biologique.consultation.id)
                    bilan_biologique.graphique = image_url
                    bilan_biologique.save()

                else:
                    return Response({"error": "Format de données invalide dans 'result' pour la génération du graphique empilé."}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({"error": f"Erreur lors de la génération du graphique empilé : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                result = bilan_biologique.result
                if isinstance(result, dict):
                    chemin_dossier = os.path.join(settings.MEDIA_ROOT, 'graphe_généré')
                    os.makedirs(chemin_dossier, exist_ok=True)
                    chemin_fichier_absolu = os.path.join(chemin_dossier, f'graphe_{patient_id}_{bilan_biologique.consultation.id}.png')
                    image_url = generer_graphe_simple(result, chemin_fichier_absolu)

                    chemin_fichier_relatif = os.path.basename(chemin_fichier_absolu)
                    image_url = os.path.join(settings.MEDIA_URL, 'graphe_généré', chemin_fichier_relatif)

                    bilan_biologique.graphique = image_url
                    bilan_biologique.save()
                else:
                    return Response({"error": "Format de données invalide dans 'result' pour la génération du graphique simple."}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({"error": f"Erreur lors de la génération du graphique simple : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        serializer = BilanBiologiqueSerializer(bilan_biologique)
        return Response(
            {"success": "Bilan biologique remplis avec succès", "bilan": serializer.data},
            status=status.HTTP_200_OK,
        )

    except BilanBiologique.DoesNotExist:
        return Response({"error": "Bilan biologique introuvable"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Erreur interne : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsMedecin])
def creer_bilan_radiologique(request):
    try:
        data = request.data
        serializer = BilanRadiologiqueSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        consultation_id = data.get("consultation")
        radiologue_id = data.get("radiologue")
        description = data.get("description")

        consultation = Consultation.objects.get(id=consultation_id)
        radiologue = Radiologue.objects.get(id=radiologue_id)

        bilan_radiologique = BilanRadiologique.objects.create(
            consultation=consultation,
            radiologue=radiologue,
            description=description,
            date=data.get("date"),
        )

        response_serializer = BilanRadiologiqueSerializer(bilan_radiologique)
        return Response({"success": "Bilan radiologique créé avec succès", "bilan": response_serializer.data},
                        status=status.HTTP_201_CREATED)

    except Consultation.DoesNotExist:
        return Response({"error": "Consultation introuvable"}, status=status.HTTP_404_NOT_FOUND)
    except Radiologue.DoesNotExist:
        return Response({"error": "Radiologue introuvable"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Erreur interne : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsRadiologue])
def ajouter_image_medicale(request):
    try:
        data = request.data
        serializer = ImageMedicalSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        bilan_radiologique_id = data.get("bilan_radiologique")
        image = data.get("image")
        notes = data.get("notes")

        bilan_radiologique = BilanRadiologique.objects.get(id=bilan_radiologique_id)

        image_medicale = ImageMedical.objects.create(
            bilan_radiologique=bilan_radiologique,
            image=image,
            notes=notes,
        )

        response_serializer = ImageMedicalSerializer(image_medicale)
        return Response({"success": "Image médicale ajoutée avec succès", "image": response_serializer.data},
                        status=status.HTTP_201_CREATED)

    except BilanRadiologique.DoesNotExist:
        return Response({"error": "Bilan radiologique introuvable"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Erreur interne : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def generer_graphe_simple(donnees, chemin_fichier):
    tests = list(donnees.keys())  
    valeurs = list(donnees.values())  

    plt.figure(figsize=(8, 6))
    plt.bar(tests, valeurs, color="#BEAEE2")
    plt.xlabel("Tests")
    plt.ylabel("Valeurs")
    plt.title(f"Résultats des tests")
    plt.xticks(rotation=45, ha='right')

    

    plt.savefig(chemin_fichier)
    plt.close()

    return os.path.join(settings.MEDIA_URL, 'graphe_généré', chemin_fichier)




def generer_graphe_empile(donnees_ancien, donnees_nouveau, patient_id, consultation_id):
    

    tests = list(donnees_ancien.keys())  
    valeurs_ancien = list(donnees_ancien.values()) 
    valeurs_nouveau = list(donnees_nouveau.values())  
 
    x = range(len(tests))

    plt.figure(figsize=(10, 6))

    plt.bar(x, valeurs_ancien, label="Bilan précédent", color="#F7DBF0")
    plt.bar(x, valeurs_nouveau, bottom=valeurs_ancien, label="Nouveau bilan", color="#BEAEE2")

    plt.xlabel("Analyses")
    plt.ylabel("Valeurs")
    plt.title(f"Évolution des analyses")
    plt.xticks(x, tests, rotation=45, ha='right')  
    plt.legend()

    chemin_dossier = os.path.join(settings.MEDIA_ROOT, 'graphe_généré')
    os.makedirs(chemin_dossier, exist_ok=True)
    chemin_fichier_absolu = os.path.join(chemin_dossier, f'graphe_empile_{patient_id}_{consultation_id}.png')
    plt.savefig(chemin_fichier_absolu)
    plt.close()

    chemin_fichier_relatif = os.path.basename(chemin_fichier_absolu)
    return os.path.join(settings.MEDIA_URL, 'graphe_généré', chemin_fichier_relatif)




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsLaborantin])
def afficher_liste_bilans(request):
    try:
        
        user = request.user
        bilans = None
        data = []


        if IsLaborantin().has_permission(request, None):
            try:
                laborantin = Laborantin.objects.get(user=user)
            except Laborantin.DoesNotExist:
                return Response({"error": "Laborantin non trouvé."}, status=status.HTTP_404_NOT_FOUND)


            bilans = BilanBiologique.objects.filter(laborantin=laborantin).order_by('-consultation__date')


        elif IsRadiologue().has_permission(request, None):
            try:
                radiologue = Radiologue.objects.get(user=user)
            except Radiologue.DoesNotExist:
                return Response({"error": "Radiologue non trouvé."}, status=status.HTTP_404_NOT_FOUND)


            bilans = BilanRadiologique.objects.filter(radiologue=radiologue).order_by('-consultation__date')


        else:
            return Response({"error": "Utilisateur non autorisé à afficher les bilans."}, status=status.HTTP_403_FORBIDDEN)


       

        data = []
        for bilan in bilans:
            patient = bilan.consultation.dpi.patient
            medecin = bilan.consultation.dpi.medecin_traitant
            data.append({
                'id_bilan': bilan.id,
                'type_bilan': bilan.test_type if bilan.test_type else None, # Gérer le cas où type_bilan est nul
                'date_creation_consultation': bilan.consultation.date,
                'patient': {
                    'id': patient.user.id,
                    'nom': patient.user.first_name,
                    'prenom': patient.user.last_name,
                },
                'medecin': {
                    'email': medecin.user.email,
                } if medecin else None, 
                'graphique': bilan.graphique,
                'resultat': bilan.result
            })

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Erreur lors de la récupération des bilans : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_bilan_biologique(request, id):
    try:
        bilan = get_object_or_404(BilanBiologique, id=id) 
    except BilanBiologique.DoesNotExist: 
        return Response({"detail": "Bilan non trouvé."}, status=status.HTTP_404_NOT_FOUND)

    if not can_get_obj(request.user, bilan):
        return Response(
            {"detail": "Vous n'êtes pas autorisé à consulter ce bilan."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = BilanBiologiqueSerializer(bilan) 

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_bilan_radiologique(request, id):
    try:
        bilan = get_object_or_404(BilanRadiologique, id=id) 
    except BilanRadiologique.DoesNotExist: 
        return Response({"detail": "Bilan non trouvé."}, status=status.HTTP_404_NOT_FOUND)

    if not can_get_obj(request.user, bilan):
        return Response(
            {"detail": "Vous n'êtes pas autorisé à consulter ce bilan."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = BilanRadiologiqueSerializer(bilan) 

    return Response(serializer.data, status=status.HTTP_200_OK)