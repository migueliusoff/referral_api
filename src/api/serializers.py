from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import User


class UserRegisterModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, label="Подтверждение пароля", write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password") != attrs.get("confirm_password"):
            raise ValidationError({"confirm_password": "Passwords don't match"})
        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password")
        extra_kwargs = {"password": {"write_only": True}}
