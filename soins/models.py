from django.db import models
from consultations.models import Consultation

class Soins(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    soins_donnés = models.TextField()
    notes = models.TextField()
    consultation = models.ForeignKey(Consultation,null=True, on_delete=models.CASCADE, related_name='soins')