import uuid

from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="обновлен")

    class Meta:
        abstract = True


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


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    objects = UserManager()
    USERNAME_FIELD = "email"

    email = models.EmailField(unique=True)
    password = models.CharField(
        max_length=128, validators=[password_validation.validate_password], verbose_name="пароль"
    )
    referrer = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="реферер", related_name="referrals"
    )
    is_staff = models.BooleanField(default=False, verbose_name="является сотрудником")

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class ReferralCode(BaseModel):
    value = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="значение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referral_codes", verbose_name="пользователь")
    expiration = models.PositiveIntegerField(
        verbose_name="срок годности в часах", validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    is_active = models.BooleanField(default=True, verbose_name="является активным")

    @property
    def is_expired(self):
        if self.created_at + timezone.timedelta(hours=self.expiration) <= timezone.now():
            return True
        return False

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        super().save(
            *args, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )
        ReferralCode.objects.filter(user=self.user).exclude(id=self.id).update(is_active=False)

    class Meta:
        verbose_name = "реферальный код"
        verbose_name_plural = "реферальные коды"
        ordering = ("-created_at",)
