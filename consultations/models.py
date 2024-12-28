from django.db import models
from dpi_manager.models import Dpi


class Frais(models.Model):
    date_echeance = models.DateTimeField()
    montant = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # 10 digits is more than enough
    details = models.TextField()


class Certificat(models.Model):
    date_demande = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()
    motif = models.TextField()


class Resume(models.Model):
    contenu = models.TextField()
    antecedants = models.TextField()


class Consultation(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    resume = models.OneToOneField(
        Resume, on_delete=models.CASCADE, null=True, related_name="consultation"
    )
    frais = models.OneToOneField(
        Frais, on_delete=models.CASCADE, null=True, related_name="consultation"
    )
    certificat = models.OneToOneField(
        Certificat, on_delete=models.CASCADE, null=True, related_name="consultation"
    )
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name="consultations")
