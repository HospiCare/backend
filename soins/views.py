from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from users.permissions import can_get_obj, IsInfirmier
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Soins
from .serializers import SoinsSerializer
from dpi_manager.models import Dpi
from django.core.exceptions import ObjectDoesNotExist

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsInfirmier])
def remplir_soins(request):
    try:
        data = request.data
        
        # Get the Dpi associated with the soins
        dpi_id = data.get('dpi')
        try:
            dpi = Dpi.objects.get(id=dpi_id)
        except ObjectDoesNotExist:
            return Response({'error': 'DPI not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare the Soins data
        soins_data = {
            'soins_donnés': data.get('soins_donnés', ''),
            'notes': data.get('notes', ''),
            'dpi': dpi.id
        }
        # Create Soins
        soins_serializer = SoinsSerializer(data=soins_data)
        if soins_serializer.is_valid():
            soins = soins_serializer.save()
            return Response({'success': 'Soins created successfully', 'soins': soins_serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(soins_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return Response({'error': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
