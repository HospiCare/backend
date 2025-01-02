from django.db import models
from django.conf import settings
from users.models import Patient, Medecin
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os


class Dpi(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='dpi')
    mutuelle = models.CharField(max_length=100)
    medecin_traitant = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, related_name='dossiers')
    telephone_personne_contact = models.CharField(max_length=15)
    cree_par = models.CharField(max_length=255, null=True, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def generate_qr_code(self):
        qr_data = f"NSS:{self.patient.NSS}"
        qr = qrcode.make(qr_data)

        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)

        qr_codes_dir = 'qr_codes'  
        os.makedirs(qr_codes_dir, exist_ok=True)  

        file_name = f"qr_code_{self.patient.NSS}.png"
        file_path = os.path.join(qr_codes_dir, file_name)

        if not default_storage.exists(file_path):  
            default_storage.save(file_path, ContentFile(img_io.getvalue()))
        else:
            print(f"Le fichier {file_path} existe déjà, aucune sauvegarde effectuée.")

        return default_storage.url(file_path)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = self.generate_qr_code()
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'dpi_manager'
