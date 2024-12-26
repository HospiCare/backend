from django.db import models
from users.models import Laborantin, Radiologue
from consultations.models import Consultation


class Bilan(models.Model):
    consultation = models.OneToOneField(
        Consultation, on_delete=models.CASCADE, related_name="%(class)s"
    )
    date = models.DateField()

    class Meta:
        abstract = True


class BilanBiologique(Bilan):
    laborantin = models.ForeignKey(Laborantin, on_delete=models.CASCADE, related_name="bilans_biologiques_laborantin")
    test_type = models.CharField(max_length=100)
    result = models.TextField()
    graphique = models.JSONField() # required data to generate the graph


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

