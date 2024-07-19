from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from apps.shared.django.models import CreatedBaseModel


class Person(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)


class ShopUser(AbstractBaseUser):
    class Type(models.TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    username = models.CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()])

    last_activity = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(db_default=False)
    telegram_id = models.BigIntegerField(blank=True, null=True, unique=True)
    person = models.OneToOneField('users.Person', models.SET_NULL, null=True, blank=True)

    type = models.CharField(max_length=25)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    language = models.ForeignKey('shops.Language', models.CASCADE)
    shop = models.ForeignKey('shops.Shop', models.CASCADE, related_name='customers')
    created_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        unique_together = [
            ('username', 'shop')
        ]


class User(AbstractBaseUser, PermissionsMixin):
    class Type(models.TextChoices):
        EMAIL = 'email', 'Email'
        TELEGRAM = 'telegram', 'Telegram'
        FACEBOOK = 'facebook', 'Facebook'

    type = models.TextField(choices=Type.choices, max_length=255)
    username = models.CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    first_name = models.CharField(max_length=255, blank=True, verbose_name='Ism')
    last_name = models.CharField(max_length=255, blank=True, verbose_name='Familya')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    language = models.ForeignKey('shops.Language', on_delete=models.CASCADE)
    public_offer = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=25, blank=True, unique=True)
    created_at = models.DateTimeField(auto_add=True)
    default_shop = models.OneToOneField('shops.Shop', models.SET_NULL, blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        unique_together = [
            ('username', 'shop')
        ]


class Plan(CreatedBaseModel):
    name = models.CharField('Nomi', max_length=150)
    code = models.CharField('Kod', max_length=150)
    description = models.TextField('Tavsif', max_length=150)
    quotas = models.ManyToManyField('users.Quotas', through='users.PlanQuotas', blank=True)


class PlanPricing(CreatedBaseModel):
    class PeriodType(models.TextChoices):
        MONTHLY = 'monthly', 'Monthly'
        ANNUAL = 'annual', 'Annual'

    name = models.CharField('Nomi', max_length=50)
    period_type = models.CharField('Davr turi', max_length=25, choices=PeriodType.choices, db_default=PeriodType.MONTHLY)
    currency = models.ForeignKey('shops.Currency', models.RESTRICT)

    price = models.PositiveIntegerField('Narxi')
    original_price = models.PositiveIntegerField('Haqiqiy narxi')
    period = models.IntegerField('Davr')
    plan = models.ForeignKey('users.Plan', models.CASCADE)


class Quotas(CreatedBaseModel):
    name = models.CharField('Nomi', max_length=150)
    description = models.TextField('Tavsif', blank=True)


class PlanQuotas(models.Model):
    plan = models.ForeignKey('users.Plan', models.CASCADE)
    quotas = models.ForeignKey('users.Quotas', models.CASCADE)
    value = models.CharField('Qiymat', max_length=50)


class PlanInvoice(CreatedBaseModel):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        COMPLETED = 'completed', 'Completed'

    price = models.CharField('Narxi', max_length=55)
    user = models.ForeignKey('users.User', models.CASCADE, related_name='plan_invoices')
    plan = models.ForeignKey('users.Plan', models.CASCADE)
    payed_at = models.DateTimeField('da toʻlangan', null=True, blank=True)
    pay_url = models.URLField('tolov url', null=True, blank=True)
    plan_extended_from = models.DateField()
    plan_extended_until = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=Status.choices, db_default=Status.NEW)


