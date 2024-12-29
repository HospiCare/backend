from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework import status
from .models import BilanBiologique, BilanRadiologique, ImageMedical
from .serializers import BilanBiologiqueSerializer,BilanRadiologiqueSerializer, ImageMedicalSerializer
from consultations.models import Consultation
from users.models import Laborantin, Radiologue
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import can_get_obj, IsMedecin,IsLaborantin,IsRadiologue

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
            date=data.get("date"),
            result=None,  # Ensure result is empty
            graphique=None  # Ensure graphique is empty
        )

        response_serializer = BilanBiologiqueSerializer(bilan_biologique)
        return Response({"success": "Bilan biologique créé avec succès", "bilan": response_serializer.data},
                        status=status.HTTP_201_CREATED)

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

@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsLaborantin])
def update_bilan_biologique(request, id):
    try:
        data = request.data
        bilan_biologique = BilanBiologique.objects.get(id=id)

        # Restrict fields for the laborantin
        allowed_fields = {"result", "graphique"}
        update_data = {key: data[key] for key in data if key in allowed_fields}

        for field, value in update_data.items():
            setattr(bilan_biologique, field, value)
        bilan_biologique.save()

        serializer = BilanBiologiqueSerializer(bilan_biologique)
        return Response(
            {"success": "Bilan biologique mis à jour avec succès", "bilan": serializer.data},
            status=status.HTTP_200_OK,
        )

    except BilanBiologique.DoesNotExist:
        return Response({"error": "Bilan biologique introuvable"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"Erreur interne : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
