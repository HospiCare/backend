from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Allow users to login and obtain a token
    """
    email = request.data.get("email", "")
    password = request.data.get("password", "")
    user = get_object_or_404(User, email=email)

    if not user.check_password(password):
        return Response(
            {"detail": "Invalid email/password."}, status=status.HTTP_404_NOT_FOUND
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
    Allow an authenticated admin to create new users (except for admin & superuser types), and superuser to create all types of users.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"detail": "A user with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.data["user_type"] in [
            "admin",
            "superuser",
        ] and not IsAdminUser().has_permission(request, None):
            return Response(
                {"detail": "Only supersuer can create admin & superuser accounts."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = User.objects.create(
            email=request.data["email"],
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            user_type=request.data.get("user_type", "patient"),
        )
        user.set_password(request.data["password"])
        user.save()

        response_serializer = UserSerializer(user)
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": response_serializer.data})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Allow an authenticated user to change heir password.
    """
    user = request.user
    current_password = request.data.get("current_password", "")
    new_password = request.data.get("new_password", "")
    confirm_password = request.data.get("confirm_password", "")

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


# TODO: profile view
@api_view(["GET"])
@permission_classes([AllowAny])
def get_profile(request, id):
    """
    Allow authunticated users to view other's profiles
    """
    return Response(
        {"detail": "NOT Implimented yet"}, status=status.HTTP_501_NOT_IMPLEMENTED
    )
