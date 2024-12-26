from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer, PatientSerializer, MedecinSerializer, \
        LaborantinSerializer, RadiologueSerializer, InfirmierSerializer, \
        LoginSerializer, FakeSerializer, ChangePasswordSerializer, UserUpdateSerializer
from .permissions import IsAdmin, can_get_obj


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Allow users to login and obtain a token
    """
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data.get("email", "")
    password = serializer.validated_data.get("password", "")

    user = get_object_or_404(User, email=email)
    if not user.check_password(password):
        return Response(
            {"detail": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserSerializer(instance=user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Allow users to logout and delete their token
    """
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdmin])
def create_account(request):
    """
    Allow an authenticated admin to create new users with their profiles (except for admin & superuser types), and superuser to create all types of users.
    """
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data.get("email")
    if User.objects.filter(email=email).exists():
        return Response(
            {"detail": "A user with this email already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user_type = serializer.validated_data.get("user_type")
    if user_type in ["admin", "superuser"] and not request.user.is_superuser:
        return Response(
            {"detail": "Only supersuer can create admin & superuser accounts."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if user_type == "patient":
        profile_serializer = PatientSerializer(data=request.data)
    elif user_type == "medecin":
        profile_serializer = MedecinSerializer(data=request.data)
    elif user_type == "laborantin":
        profile_serializer = LaborantinSerializer(data=request.data)
    elif user_type == "radiologue":
        profile_serializer = RadiologueSerializer(data=request.data)
    elif user_type == "infirmier":
        profile_serializer = InfirmierSerializer(data=request.data)
    elif user_type == "superuser":
        serializer.validated_data["is_staff"] = True
        serializer.validated_data["is_superuser"] = True
        profile_serializer = FakeSerializer(data=request.data)
    else:
        profile_serializer = FakeSerializer(data=request.data)

    if not profile_serializer.is_valid():
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = serializer.create(serializer.validated_data)
        profile_serializer.validated_data['user'] = user
        profile_serializer.create(profile_serializer.validated_data)

        response_serializer = UserSerializer(user)
        return Response({"detail": f"{user_type} successfuly created", "user": response_serializer.data})

    except Exception:
        return Response(
            {"detail": "An error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Allow an authenticated user to change heir password.
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    current_password = serializer.validated_data.get("current_password")
    new_password = serializer.validated_data.get("new_password")
    confirm_password = serializer.validated_data.get("confirm_password")

    user = request.user
    if not user.check_password(current_password):
        return Response(
            {"detail": "Current password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if new_password != confirm_password:
        return Response(
            {"detail": "New password and confirmation do not match."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)
    user.save()

    return Response(
        {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
    )


@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdmin]) # only admins can change profiles
def change_profile(request, id):
    """
    Allow admins to update user profile
    """
    user = get_object_or_404(User, id=id)

    serializer = UserUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try: # setting a unique feild with an existing value will trigger an exception
        for field_name, value in serializer.validated_data.items():
            if hasattr(user, field_name):
                setattr(user, field_name, value) 

        user.save()

    except Exception:
        return Response(
            {"detail": "An error occurred. Make sure you are respecting unicity..."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    res_serializer = UserSerializer(instance=user)
    return Response({"user": res_serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    """
    Allow authunticated users to view other's profiles
    """
    user = get_object_or_404(User, id=id)
    if not can_get_obj(request.user, user):
        return Response({"details": "You are not allowed to view details about this user"})

    serializer = UserSerializer(instance=user)
    return Response({"user": serializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Allow authunticated user to view their profile
    """
    serializer = UserSerializer(instance=request.user)
    return Response({"user": serializer.data})
