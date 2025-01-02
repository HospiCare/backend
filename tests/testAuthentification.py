import pytest
from rest_framework.test import APIClient
from users.models import User, Medecin  
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user_fixture():
    
    user = User.objects.create_user(
        email="medecin@example.com",
        password="testpassword",
        first_name="Medecin",
        last_name="Test",
        user_type="medecin",
    )
    Medecin.objects.create(
        user=user,
        date_naissance="1990-01-01",
        adresse="test adresse",
        telephone="0665990290"
    )
    return user


@pytest.mark.django_db
def test_login_with_valid_credentials(api_client, create_user_fixture):
    
    response = api_client.post('/user/login/', {'email': 'medecin@example.com', 'password': 'testpassword'})
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data
    assert response.data['token'] is not None
    assert 'user' in response.data
    assert response.data['user']['email'] == 'medecin@example.com'


@pytest.mark.django_db
def test_login_with_invalid_credentials(api_client, create_user_fixture):
    
    response = api_client.post('/user/login/', {'email': 'medecin@example.com', 'password': 'wrongpassword'})
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['detail'] == 'Wrong password.'


@pytest.mark.django_db
def test_login_with_nonexistent_user(api_client):
  
    response = api_client.post('/user/login/', {'email': 'nonexistentuser@example.com', 'password': 'testpassword'})
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'detail' in response.data
    # Modifier l'assertion en fonction du message exact retourné par Django
    assert response.data['detail'] == 'No User matches the given query.'


@pytest.mark.django_db
def test_login_with_missing_fields(api_client):
    
    # Test sans email
    response = api_client.post('/user/login/', {'password': 'testpassword'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

    # Test sans mot de passe
    response = api_client.post('/user/login/', {'email': 'medecin@example.com'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password' in response.data
