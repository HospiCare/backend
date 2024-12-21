from django.db import models
from django.conf import settings
from users.models import Patient,Medecin


class Dpi(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='dpi')
    mutuelle = models.CharField(max_length=100)
    medecin_traitant = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, related_name='dossiers')
    telephone_personne_contact = models.CharField(max_length=15)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Utilisez AUTH_USER_MODEL au lieu de User
        on_delete=models.SET_NULL,
        null=True,
        related_name='dpi_crees'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'dpi_manager'  
