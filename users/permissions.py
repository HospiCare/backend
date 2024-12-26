from rest_framework.permissions import BasePermission

from consultations.models import Consultation, Frais, Certificat, Resume
from dpi_manager.models import Dpi
from users.models import Patient


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


def can_get_obj(user, obj):
    user_id = user.id
    user_type = user.user_type

    if user_type in ["superuser", "admin"]:
        return True

    if isinstance(obj, Consultation):
        if user_type == "medecin":
            return True

        dpi = Dpi.objects.get(id=obj.dpi_id)
        patient = Patient.objects.get(id=dpi.patient_id)

        return user_id == patient.user_id

    if isinstance(obj, Patient):
        if user_type != "patient":
            return True

        return user_id == obj.user_id

    if isinstance(obj, Frais):
        return can_get_obj(user, obj.consultation)

    if isinstance(obj, Resume):
        return can_get_obj(user, obj.consultation)

    if isinstance(obj, Certificat):
        return can_get_obj(user, obj.consultation)

    raise Exception("Model Permission not implimented!")
    return False
