from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    class Type(models.TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    type = models.TextField(choices=Type.choices, max_length=255)
    username = models.CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(db_default=False)
    last_active = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey('shops.Language', on_delete=models.CASCADE)
    public_offer = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=25, blank=True, unique=True)
    created_at = models.DateTimeField(auto_add=True)
    telegram_id = models.BigIntegerField(blank=True, null=True)
    default_shop = models.OneToOneField('shops.Shop', models.SET_NULL, blank=True, null=True)
    shop = models.ForeignKey('shops.Shop', models.CASCADE, blank=True, null=True, related_name='customers')

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        unique_together = [
            ('username', 'shop')
        ]




