from django.db import models
from django.conf import settings
from users.models import Patient,Medecin
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Dpi(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='dpi')
    mutuelle = models.CharField(max_length=100)
    medecin_traitant = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, related_name='dossiers')
    telephone_personne_contact = models.CharField(max_length=15)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.SET_NULL,
        null=True,
        related_name='dpi_crees'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:  
            self.qr_code = self.generate_qr_code()
        

    def generate_qr_code(self):
        """Générer un QR code à partir du NSS du patient."""
        qr_data = f"NSS:{self.patient.NSS}"  
        qr = qrcode.make(qr_data)

        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)

        qr_code_file = InMemoryUploadedFile(img_io, None, f"qr_code_{self.patient.NSS}.png", 'image/png', img_io.tell(), None)
        return qr_code_file

    class Meta:
        app_label = 'dpi_manager'

 