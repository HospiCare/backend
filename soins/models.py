from django.db import models
from consultations.models import Consultation
from users.models import Infirmier
class Soins(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    soins_donnés = models.TextField()
    notes = models.TextField()
    consultation = models.OneToOneField(Consultation, null=True, on_delete=models.CASCADE, related_name='soins')
    infirmier = models.ForeignKey(Infirmier,null=True,  on_delete=models.CASCADE)
