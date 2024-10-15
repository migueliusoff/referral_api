from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.model(email=email, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    USERNAME_FIELD = "email"

    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=128, validators=[password_validation.validate_password], verbose_name="пароль"
    )
    referrer = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="реферер", related_name="referrals"
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
