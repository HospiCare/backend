from django.db import models
from dpi_manager.models import Dpi

class Soins(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    soins_donnés = models.TextField()
    notes = models.TextField()
    dpi = models.ForeignKey(Dpi, on_delete=models.CASCADE, related_name='soins')
