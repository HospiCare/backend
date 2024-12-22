"""
User Model is defined here. It's purpose is use in authentication,
diffrent user types should be implimented as profiles where the
associated user is a OneToOne field

les type d'utilisateur:
    'superuser': l'administrateur de system
    'admin': le personnel administratif
    'medecin'
    'patient'
    'infirmier'
    'laborantin'
    'radiologue'

example of implementing Profiles:
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    nss = models.PositiveIntegerField(unique=True) # Numero de securite social
    birthdate = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    ...

"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


USER_TYPE_CHOICES = [
    ("superuser", "Administrateur system"),
    ("admin", "Personnel Adminstratif"),
    ("medecin", "Medecin"),
    ("patient", "Patient"),
    ("infirmier", "Infirmier"),
    ("laborantin", "Laborantin"),
    ("radiologue", "Radiologue"),
]


class UserManager(BaseUserManager):
    """
    UserManager (extends Django's BaseUserManager)
    here create_user and create_superuser are implimented
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    User Model (extends Django's AbstractUser)
    - username field is disabled and replaced with email
    - first_name & last_name fields added
    - user_type: used to determine the permission (& type) of the user
    """

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "user_type"]


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=10)
    NSS = models.CharField(max_length=50, unique=True) #Numéro de Sécurité Sociale

    def __str__(self):
        """Retourne le nom et le prénom d'un objet de type Patient"""
        return f"{self.user.first_name} {self.user.last_name}"


class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medecin_profile')
    date_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=10)

     

    def __str__(self):
        """Retourne le nom et le prénom d'un objet de type Médecin"""
        return f"Dr. {self.user.first_name} {self.user.last_name}"
