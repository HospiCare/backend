import pytest
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Medecin, Patient
from dpi_manager.models import Dpi
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def medecin_fixture(db):
    user = get_user_model().objects.create_user(
        email="medecin@example.com",
        password="testpassword",
        first_name="Medecin",
        last_name="Test",
        user_type="medecin"
    )
    Medecin.objects.create(
        user=user,
        date_naissance="1985-01-01",
        adresse="Adresse Médecin",
        telephone="0665990290"
    )
    return user  



@pytest.mark.django_db
def test_creer_dpi_valid_data(api_client, medecin_fixture):
   
    api_client.force_authenticate(user=medecin_fixture)

    payload = {
        "nom_patient": "test",
        "prenom_patient": "patient",
        "date_naissance": "1990-01-01",
        "adresse_patient": "Adresse Patient",
        "telephone_patient": "0665990290",
        "email_patient": "test@patient.com",
        "NSS": "11110000",
        "mot_de_passe": "securepassword",
        "medecin_id": medecin_fixture.id,  
        "mutuelle": "Mutuelle A",
        "telephone_personne_contact": "0655555555"
    }

    response = api_client.post("/dpi_manager/creer_dpi/", payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] == "DPI créé avec succès"
    assert "dpi" in response.data


@pytest.mark.django_db
def test_creer_dpi_permission_refusee(api_client, medecin_fixture):
   
    user = get_user_model().objects.create_user(
        email="user@example.com",
        password="password",
        user_type="patient"
    )
    Patient.objects.create(
        user=user,
        date_naissance="1980-01-01",
        adresse="Adresse Patient",
        telephone="0665990290",
        NSS="1234567890123"
    )
    api_client.force_authenticate(user=user)

    payload = {
        "nom_patient": "Patient",
        "prenom_patient": "Test",
        "date_naissance": "1990-01-01",
        "adresse_patient": "Adresse Patient",
        "telephone_patient": "0664329087",
        "email_patient": "patient@example.com",
        "NSS": "1234567890123",
        "mot_de_passe": "securepassword",
        "medecin_id": medecin_fixture.id,  
        "mutuelle": "Mutuelle A",
        "telephone_personne_contact": "0655555555"
    }

    response = api_client.post("/dpi_manager/creer_dpi/", payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data["error"] == "Seuls un médecin ou un administrateur peuvent créer un DPI."


@pytest.mark.django_db
def test_creer_dpi_medecin_inexistant(api_client, medecin_fixture):
    """
    Teste la création d'un DPI avec un médecin inexistant
    """
    api_client.force_authenticate(user=medecin_fixture)

    payload = {
        "nom_patient": "Patient",
        "prenom_patient": "Test",
        "date_naissance": "1990-01-01",
        "adresse_patient": "Adresse Patient",
        "telephone_patient": "0668242904",
        "email_patient": "patient@example.com",
        "NSS": "1234567890123",
        "mot_de_passe": "securepassword",
        "medecin_id": 9999,  # ID invalide
        "mutuelle": "Mutuelle A",
        "telephone_personne_contact": "0655555555"
    }

    response = api_client.post("/dpi_manager/creer_dpi/", payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Médecin avec ID 9999 introuvable."



@pytest.mark.django_db
def test_creer_dpi_donnees_invalides(api_client, medecin_fixture):
    """
    Teste la création d'un DPI avec des données invalides
    """
    api_client.force_authenticate(user=medecin_fixture)

    payload = {
        "nom_patient": "",
        "prenom_patient": "Test",
        # Champ "date_naissance" manquant
        "adresse_patient": "Adresse Patient",
        "telephone_patient": "0600000000",
        "email_patient": "patient@example.com",
        "NSS": "1234567890123",
        "mot_de_passe": "securepassword",
        "medecin_id": 1,
        "mutuelle": "Mutuelle A",
        "telephone_personne_contact": "0655555555"
    }

    response = api_client.post("/dpi_manager/creer_dpi/", payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "date_naissance" in response.data
