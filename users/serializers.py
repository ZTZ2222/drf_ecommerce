from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Address, User
from .exceptions import InvalidCredentialsException, AccountDisabledException


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, validated_data):
        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError("Passwords do not match!")

        password = validated_data.get("password1", "")
        if len(password) < 8:
            raise serializers.ValidationError(
                "Passwords must be at least 8 characters!"
            )

        return validated_data

    def create(self, validated_data) -> User:
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        return User.objects.create_user(password=password, **validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        else:
            user = authenticate(email=email, password=password)

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        validated_data["user"] = user
        return validated_data


class AddressWriteSerializer(serializers.ModelSerializer):
    """Serializer class to seralize address"""

    class Meta:
        model = Address
        fields = "__all__"


class AddressReadOnlySerializer(AddressWriteSerializer):
    """Serializer class to seralize Address model with read only fields"""

    user = serializers.CharField(source="user.email", read_only=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to seralize User model
    """

    addresses = AddressReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "addresses")
