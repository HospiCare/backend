import pytest
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Patient, Medecin  
from dpi_manager.models import Dpi
from django.contrib.auth import get_user_model
from django.conf import settings
import tempfile
import shutil
import os
from rest_framework import status
import shutil
import tempfile


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def medecin_fixture(db):
    user = get_user_model().objects.create_user(
        email="medecin@example.com",
        password="passwordmedecin",
        first_name="Medecin",
        last_name="Test",
        user_type="medecin"
    )
    medecin =Medecin.objects.create(
        user=user,
        date_naissance="1985-01-01",
        adresse="Adresse Médecin",
        telephone="0665990290"
    )
    return medecin  


@pytest.fixture
def patient_fixture(db):
    user = get_user_model().objects.create_user(
        email="patient@example.com",
        password="passwordpatient",
        first_name="Patient",
        last_name="Test",
        user_type="patient"
    )
    patient = Patient.objects.create(
        user=user,
        date_naissance="1980-01-01",
        adresse="Adresse Patient",
        telephone="0665990290",
        NSS="11223344556677"
    )
    return patient


@pytest.fixture
def dpi_fixture(medecin_fixture, patient_fixture):
    dpi = Dpi.objects.create(
        patient=patient_fixture,
        mutuelle="Mutuelle Test",
        medecin_traitant=medecin_fixture,
        telephone_personne_contact="0678998877"
    )
    return dpi

@pytest.mark.django_db
def test_rechercher_par_qrcode_valid(medecin_fixture, dpi_fixture, api_client):
   
    api_client.force_authenticate(user=medecin_fixture.user)

    qr_code_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', f"qr_code_{dpi_fixture.patient.NSS}.png")


    with open(qr_code_path, 'rb') as image_file:
        response = api_client.post(
            '/dpi_manager/rechercher_dpi_par_QRcode/', 
            {'qr_code': image_file},
            format='multipart'
        )

    assert response.status_code == status.HTTP_200_OK
    assert 'success' in response.data
    assert response.data['success'] == 'DPI trouvé'




@pytest.mark.django_db
def test_rechercher_par_qrcode_no_file(medecin_fixture, api_client):
        
        api_client.force_authenticate(user=medecin_fixture.user)

        # Tester sans fichier
        response = api_client.post('/dpi_manager/rechercher_dpi_par_QRcode/', {}, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Aucune image de QR code fournie'




@pytest.mark.django_db
def test_rechercher_par_qrcode_invalid_format(medecin_fixture, api_client):
    api_client.force_authenticate(user=medecin_fixture.user)

    qr_code_path = os.path.join(settings.BASE_DIR, 'tests', 'qr_codes_test', 'Invalid_format.png')

    with open(qr_code_path, 'rb') as image_file:
        response = api_client.post(
            '/dpi_manager/rechercher_dpi_par_QRcode/', 
            {'qr_code': image_file},
            format='multipart'
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'QR code invalide' in response.data['error']




@pytest.mark.django_db
def test_rechercher_par_qrcode_dpi_not_found(medecin_fixture, api_client):
        
        api_client.force_authenticate(user=medecin_fixture.user)

        qr_code_path = os.path.join(settings.BASE_DIR, 'tests', 'qr_codes_test', 'DPI_not_found.png')


        with open(qr_code_path, 'rb') as image_file:
             response = api_client.post(
            '/dpi_manager/rechercher_dpi_par_QRcode/', 
            {'qr_code': image_file},
            format='multipart'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == 'Patient non trouvé avec ce NSS'


   



@pytest.fixture(scope='function', autouse=True)
def temp_media_root():
    '''
        Fonction de nettoyage apres les tests
    '''
    original_media_root = settings.MEDIA_ROOT

    temp_dir = tempfile.mkdtemp()
    settings.MEDIA_ROOT = temp_dir

    yield  

    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            os.remove(os.path.join(root, file))
    shutil.rmtree(temp_dir, ignore_errors=True)

    qr_codes_path = os.path.join(settings.BASE_DIR, 'tests', 'qr_codes')
    if os.path.exists(qr_codes_path):
        shutil.rmtree(qr_codes_path, ignore_errors=True)

    settings.MEDIA_ROOT = original_media_root
