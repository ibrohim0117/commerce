from django.db import models

from apps.shared.django.models import CreatedBaseModel


# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name='nomi')

    class Meta:
        verbose_name = 'Davlat'
        verbose_name_plural = 'Davlatlar'


class Language(models.Model):
    title = models.CharField(max_length=255, verbose_name='Nomi')
    code = models.CharField(max_length=255, verbose_name='Kodi')
    icon = models.CharField(max_length=255, verbose_name='Belgisi')


class ShopCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nomi')

    class Meta:
        verbose_name = 'Do\'kon toifasi'
        verbose_name_plural = 'Do\'kon toifalari'

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nomi')
    order = models.PositiveSmallIntegerField(default=1, db_default=1, verbose_name='Rangi')

    class Meta:
        verbose_name = 'Pul birligi'
        verbose_name_plural = 'Pul birliklari'

    def __str__(self):
        return self.name


class Shop(CreatedBaseModel):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = models.CharField(max_length=255, verbose_name='Do\'kon nomi')
    phone = models.CharField(max_length=255, verbose_name='Beznis telefon raqam')
    phone_number = models.CharField(max_length=255, verbose_name='Telefon raqam')

    country = models.ForeignKey('shops.Country', models.CASCADE, verbose_name='Ro\'yxatdan o\'tgan davlat')
    languages = models.ManyToManyField('shops.Language', blank=True, verbose_name='Til')
    services = models.ManyToManyField('orders.Service', through='orders.ShopService')
    category = models.ForeignKey('shops.ShopCategory', models.CASCADE, verbose_name='Kategoryalar')
    status = models.CharField(max_length=10, choices=Status.choices, db_default=Status.ACTIVE)
    currency = models.ForeignKey("shops.Currency", models.CASCADE, verbose_name="Pul birligi")
    plan = models.ForeignKey('users.Plan', models.CASCADE, related_name='shops')

    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    start_at = models.TimeField(null=True, blank=True, verbose_name='Dan')
    end_at = models.TimeField(null=True, blank=True, verbose_name='Gacha')
    has_terminal = models.BooleanField(db_default=True)
    about_use = models.TextField(blank=True, null=True, verbose_name='Biz haqimizda')
    facebook = models.URLField(max_length=255, blank=True, null=True, verbose_name='Facebook')
    instagram = models.URLField(max_length=255, blank=True, null=True, verbose_name='Instagram')
    telegram = models.URLField(max_length=255, blank=True, null=True, verbose_name='Telegram')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Elektron pochta')
    address = models.TextField(blank=True, null=True, verbose_name='Manzil')
    is_new_products_show = models.BooleanField(db_default=True, default=False, verbose_name='Ommabop'
                                                'mahsulotlar sahifasini ko\'r satish')

    class TemplateColor(models.Model):  # ✅
        name = models.CharField(max_length=55, verbose_name='Nomi')
        color = models.CharField(max_length=55, verbose_name='Rangi')

        class Meta:
            verbose_name = 'Shablon rangi'
            verbose_name_plural = 'Shablon ranglari'

        def __str__(self):
            return self.name