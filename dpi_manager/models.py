from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    NSS = models.CharField(max_length=50, unique=True) #Numéro de Sécurité Sociale
    mot_de_passe = models.CharField(max_length=128)  

    class Meta:
        app_label = 'dpi_manager'  

    def __str__(self):
        """Retourne le nom et le prénom d'un objet de type Patient"""
        return f"{self.nom} {self.prenom}"

    def set_password(self, raw_password):
        """Hash et stocke le mot de passe."""
        self.mot_de_passe = make_password(raw_password)

    def check_password(self, raw_password):
        """Vérifie si un mot de passe brut correspond au mot de passe hashé."""
        return check_password(raw_password, self.mot_de_passe)


class Medecin(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)    
    mot_de_passe = models.CharField(max_length=128)  

    class Meta:
        app_label = 'dpi_manager'  

    def __str__(self):
        """Retourne le nom et le prénom d'un objet de type Médecin"""
        return f"Dr. {self.nom} {self.prenom}"

    def set_password(self, raw_password):
        """Hash et stocke le mot de passe."""
        self.mot_de_passe = make_password(raw_password)

    def check_password(self, raw_password):
        """Vérifie si un mot de passe brut correspond au mot de passe hashé."""
        return check_password(raw_password, self.mot_de_passe)


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

        super().save(*args, **kwargs)

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
