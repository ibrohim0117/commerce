from django.db import models

from apps.shared.django.models import CreatedBaseModel


class PromoCode(CreatedBaseModel):
    class Type(models.TextChoices):
        FREE_DELIVERY = 'free_delivery', 'Free delivery'
        DISCOUNT = 'discount', 'Discount'

    type = models.CharField(max_length=255, choices=Type.choices, default=Type.FREE_DELIVERY)
    active = models.BooleanField(default=True)
    code = models.CharField(max_length=255, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    limit = models.IntegerField()
    percent = models.IntegerField(default=0)
    used_quantity = models.PositiveIntegerField()
    shop = models.ForeignKey('shops.Shop', models.CASCADE, related_name='promo_codes')

    class Meta:
        verbose_name = 'Promo kod'
        verbose_name_plural = 'Promo kodlar'


class ShopService(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        NOT_EXISTS = 'not_exists', 'Not exists'

    shop = models.ForeignKey('shops.Shop', models.CASCADE)
    service = models.ForeignKey('shops.Shop', models.CASCADE)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.INACTIVE)


class Service(models.Model):
    class Type(models.TextChoices):
        INTERNAL = 'internal', 'Internal service'
        INPLACE = 'inplace', 'Inplace'
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web',
        INSTAGRAM = 'instagram', 'Instagram'

    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=Type.choices)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = [
            ('code', 'type')
        ]
