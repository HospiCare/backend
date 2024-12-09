import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_fake(api_client):
    url = reverse('fake_endpoint')
    response = api_client.get(url)
    assert response.status_code == 200

