from django.db import models
from users.models import Laborantin, Radiologue
from consultations.models import Consultation


class Bilan(models.Model):
    consultation = models.OneToOneField(
        Consultation, on_delete=models.CASCADE, related_name="%(class)s"
    )
    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class BilanBiologique(Bilan):
    laborantin = models.ForeignKey(Laborantin, on_delete=models.CASCADE, related_name="bilans_biologiques_laborantin")
    TYPE_BILAN_CHOICES = [
        ('Bilan sanguin', 'Bilan sanguin'),
        ('Bilan d\'urine', 'Bilan d\'urine'),
        ('Bilan hepatique', 'Bilan hépatique'),
        ('Bilan renal', 'Bilan rénal'),
    ]

    test_type = models.CharField(max_length=100, choices=TYPE_BILAN_CHOICES, default='Bilan sanguin') 
    result = models.JSONField(default=dict, blank=True, null=True)  # Utilisation de JSONField pour stocker les résultats comme dictionnaire
    graphique = models.JSONField(null=True, blank=True) 


class BilanRadiologique(Bilan):
    radiologue = models.ForeignKey(Radiologue, on_delete=models.CASCADE, related_name="bilans_radiologiques_radiologue")
    description = models.TextField()


class ImageMedical(models.Model):
    bilan_radiologique = models.OneToOneField(
        BilanRadiologique, on_delete=models.CASCADE, related_name="image_medical"
    )
    image = models.ImageField() # for securtiy reasons this shouldn't be uploaded directrly
    uploaded_at = models.DateTimeField(auto_now_add=True)  
    notes = models.TextField(blank=True, null=True)  

