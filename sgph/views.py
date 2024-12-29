from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ordonnance, Medicament
from .serializers import OrdonnanceSerializer, MedicamentSerializer
from consultations.models import Consultation
from django.core.exceptions import ObjectDoesNotExist

@api_view(["POST"])
def create_ordonnance(request):
    try:
        data = request.data

        # Get Consultation
        consultation_id = data.get("consultation")
        try:
            consultation = Consultation.objects.get(id=consultation_id)
        except ObjectDoesNotExist:
            return Response({'error': 'Consultation not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare Ordonnance data (without medicaments)
        ordonnance_data = {
            "consultation": consultation.id,
            "validated": data.get("validated", False),
            "notes": data.get("notes", ''),
        }

        # Create Ordonnance
        ordonnance_serializer = OrdonnanceSerializer(data=ordonnance_data)
        if ordonnance_serializer.is_valid():
            ordonnance = ordonnance_serializer.save()

            # Link existing Medicaments (do not create new ones)
            medicament_ids = data.get('medicaments', [])
            if medicament_ids:
                for medicament_id in medicament_ids:
                    try:
                        medicament = Medicament.objects.get(id=medicament_id)
                        ordonnance.medicaments.add(medicament)
                    except Medicament.DoesNotExist:
                        return Response({'error': f'Medicament with ID {medicament_id} not found.'},
                                        status=status.HTTP_400_BAD_REQUEST)

            # Return success response
            return Response({'success': 'Ordonnance created successfully', 'ordonnance': ordonnance_serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(ordonnance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(["POST"])
def create_medicament(request):
    try:
        data = request.data

        # Serialize and Create Medicament
        medicament_serializer = MedicamentSerializer(data=data)
        if medicament_serializer.is_valid():
            medicament_serializer.save()
            return Response({'success': 'Medicament created successfully', 'medicament': medicament_serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(medicament_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)