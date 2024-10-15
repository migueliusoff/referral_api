from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import ReferralCode, User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")
        extra_kwargs = {"id": {"read_only": True}}


class UserRegisterModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, label="Подтверждение пароля", write_only=True)
    referral_code = serializers.CharField(required=False, write_only=True, label="реферальный код")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("password") != attrs.get("confirm_password"):
            raise ValidationError({"confirm_password": "Пароли не совпадают"})
        validate_password(attrs["password"])
        return attrs

    def validate_referral_code(self, referral_code):
        code_qs = ReferralCode.objects.filter(value=referral_code, is_active=True)
        if not code_qs.exists():
            raise ValidationError("Реферальный код неверен или неактивен")

        if code_qs.first().is_expired:
            raise ValidationError("Реферальный код неверен или неактивен")

        return referral_code

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        referral_code = validated_data.pop("referral_code", None)
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        if referral_code:
            user.referrer = ReferralCode.objects.get(value=referral_code).user
        user.save()
        return user

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password", "referral_code", "referrer")
        extra_kwargs = {"password": {"write_only": True}, "referrer": {"read_only": True}}


class ReferralCodeCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ("user", "value", "expiration")
        extra_kwargs = {"user": {"read_only": True}, "value": {"read_only": True}}

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ReferralCodeListModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = ReferralCode
        fields = ("id", "user", "value", "expiration", "is_active", "is_expired")
