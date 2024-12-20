from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ["id", "password", "email", "first_name", "last_name", "user_type"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
