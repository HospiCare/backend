from rest_framework.permissions import BasePermission

from consultations.models import Consultation, Frais, Certificat, Resume
from dpi_manager.models import Dpi
from users.models import Patient, User

class IsAdmin(BasePermission):
    """
    Custom permission to allow "les personnels adminstratifs" to create accounts
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type in ["superuser", "admin"]


class IsMedecin(BasePermission):
    """
    Custom permission to destinguish "medecin" from other users
    """

    def has_permission(self, request, view):
        if IsAdmin().has_permission(request, view):
            return True

        user = request.user
        return user.is_authenticated and user.user_type == "medecin"
    
class IsLaborantin(BasePermission):
    """
    Custom permission to destinguish "Laborantin" from other users
    """

    def has_permission(self, request, view):
        if IsAdmin().has_permission(request, view):
            return True

        user = request.user
        return user.is_authenticated and user.user_type == "laborantin"

class IsRadiologue(BasePermission):
    """
    Custom permission to destinguish "Radiologue" from other users
    """

    def has_permission(self, request, view):
        if IsAdmin().has_permission(request, view):
            return True

        user = request.user
        return user.is_authenticated and user.user_type == "radiologue"
class IsInfirmier(BasePermission):
    """
    Custom permission to destinguish "Infirmier" from other users
    """

    def has_permission(self, request, view):
        if IsAdmin().has_permission(request, view):
            return True

        user = request.user
        return user.is_authenticated and user.user_type == "infirmier"

# TODO: use polymorphism instead!
def can_get_obj(user, obj):
    user_id = user.id
    user_type = user.user_type

    if user_type in ["superuser", "admin"]:
        return True

    if isinstance(obj, User):
        if user_type == "patient" and obj.user_type == "patient" and user_id != obj.id:
            return False
        return True

    if isinstance(obj, Patient):
        if user_type != "patient":
            return True

        return user_id == obj.user_id

    if isinstance(obj, Consultation):
        if user_type == "medecin":
            return True

        dpi = Dpi.objects.get(id=obj.dpi_id)
        patient = Patient.objects.get(id=dpi.patient_id)

        return user_id == patient.user_id

    if isinstance(obj, Frais):
        return can_get_obj(user, obj.consultation)

    if isinstance(obj, Resume):
        return can_get_obj(user, obj.consultation)

    if isinstance(obj, Certificat):
        return can_get_obj(user, obj.consultation)


    raise Exception(f"{obj.__class__} Permission not implimented!")
    return False