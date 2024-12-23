from django.db import models


class Ordonnance(models.Model):
    validated = models.BooleanField(default=False)
    notes = models.TextField(blank=True)


class Medicament(models.Model):
    ordonnance = models.ForeignKey(
        Ordonnance, on_delete=models.CASCADE, related_name='medicaments'
    )
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.IntegerField()
