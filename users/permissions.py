from rest_framework.permissions import BasePermission
from bilan.models import *
from consultations.models import *
from users.models import *
from abc import ABC, abstractmethod

class UserTypePermission(BasePermission):  
    """
    Classe de base pour les permissions par type d'utilisateur.
    """
    user_type = None  

    def has_permission(self, request, view):
        if self.user_type is None:
            raise NotImplementedError("user_type must be defined in subclasses.")

        if request.user.is_authenticated and request.user.user_type in self.user_type:
            return True
        return False

class IsAdmin(UserTypePermission):
    user_type = ["superuser", "admin"] 

class IsMedecin(UserTypePermission):
    user_type = ["medecin"]

class IsLaborantin(UserTypePermission):
    user_type = ["laborantin"]

class IsRadiologue(UserTypePermission):
    user_type = ["radiologue"]

class IsInfirmier(UserTypePermission):
    user_type = ["infirmier"]


class ObjectPermissionChecker(ABC):
    @abstractmethod
    def has_object_permission(self, user, obj):
        pass

class ConsultationPermissionChecker(ObjectPermissionChecker):
    def has_object_permission(self, user, consultation):
        if user.user_type in ["superuser", "admin", "medecin"]:
            return True

        dpi = Dpi.objects.get(id=consultation.dpi_id)
        patient = Patient.objects.get(id=dpi.patient_id)
        return user.id == patient.user_id

class FraisPermissionChecker(ObjectPermissionChecker):
    def has_object_permission(self, user, frais):
        return can_get_obj(user, frais.consultation)

class ResumePermissionChecker(ObjectPermissionChecker):
    def has_object_permission(self, user, resume):
        return can_get_obj(user, resume.consultation)

class CertificatPermissionChecker(ObjectPermissionChecker):
    def has_object_permission(self, user, certificat):
        return can_get_obj(user, certificat.consultation)

class BilanBiologiquePermissionChecker(ObjectPermissionChecker):
    def has_object_permission(self, user, bilan):
        if user.user_type in ["superuser", "admin","laborantin"]:
            return True
        dpi = bilan.consultation.dpi
        patient = dpi.patient
        medecin = bilan.consultation.dpi.medecin_traitant
        return user == patient.user or user == medecin.user

class BilanRadiologiquePermissionChecker(ObjectPermissionChecker):
    def has_object_permission(self, user, bilan):
        if user.user_type in ["superuser", "admin","radiologue"]:
            return True
        dpi = bilan.consultation.dpi
        patient = dpi.patient
        medecin = bilan.consultation.dpi.medecin_traitant
        return user == patient.user or user == medecin.user

def can_get_obj(user, obj):
    permission_checker = {
        Consultation: ConsultationPermissionChecker(),
        Frais: FraisPermissionChecker(),
        Resume: ResumePermissionChecker(),
        Certificat: CertificatPermissionChecker(),
        BilanBiologique: BilanBiologiquePermissionChecker(),
        BilanRadiologique: BilanRadiologiquePermissionChecker(),
    }.get(obj.__class__)

    if permission_checker:
        return permission_checker.has_object_permission(user, obj)
    
    if isinstance(obj, User): 
        return True

    raise NotImplementedError(f"Permission for {obj.__class__.__name__} not implemented")