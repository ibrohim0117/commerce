from django.db import models

from apps.shared.django.models import CreatedBaseModel


class Order(models.Model):
    class Status(models.TextChoices):
        IN_PROCESSING = 'in_processing', 'In Process'
        CANCELLED = 'cancelled', 'Cancelled'
        CONFIRMED = 'confirmed', 'Confirmed'
        PERFORMING = 'performing', 'Performing'
        PERFORMED = 'performed', 'Performed'
        REFUNDED = 'refunded', 'Refunded'

    class Type(models.TextChoices):
        TELEGRAM = 'telegram', 'Telegram'
        WEB = 'web', 'Web'

    class DeliveryType(models.TextChoices):
        ONLINE_DELIVERY = 'online_delivery', 'Online Delivery'
        DELIVERY = 'delivery', 'Delivery'
        PICKUP = 'pickup', 'Pickup'

    delivery_price = models.DecimalField('Yetkazib berish narxi', null=True, blank=True, decimal_places=2, max_digits=15)
    # user = ForeignKey('users.ShopUser', SET_NULL, null=True, blank=True, verbose_name='Teligram chat id')
    payment = models.ForeignKey('orders.ShopService', models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField('Order Statusi', max_length=20, choices=Status.choices)
    paid = models.BooleanField("To'lov qilingan yoki yo'qligi", db_default=False)

    promo_code = models.ForeignKey('orders.PromoCode', models.SET_NULL, null=True, blank=True, related_name='orders')
    note = models.TextField('Description', null=True, blank=True)
    delivery_date = models.DateTimeField('Yetkazib berish vaqti', null=True, blank=True)
    delivery_type = models.CharField(max_length=50, choices=DeliveryType.choices)
    order_type = models.CharField(max_length=20, choices=Type.choices)

    is_archived = models.BooleanField('Arxivlangan buyurtmalar', db_default=False)
    yandex_taxi_link = models.CharField(max_length=255, null=True, blank=True)
    currency = models.ForeignKey('shops.Currency', models.RESTRICT, related_name='orders')
    address = models.CharField('Manzil', max_length=255, null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    entrance = models.CharField('Kirish joyi', max_length=50, null=True, blank=True)
    door_phone = models.CharField('eshik telfon raqami', max_length=50, null=True, blank=True)
    floor_number = models.IntegerField('Qavat raqami', null=True, blank=True)
    apartment_number = models.IntegerField('kvartera raqami', null=True, blank=True)

    first_name = models.CharField('Haridorni ismi', max_length=50)  # register qilgan paytdagi ismni oladi
    last_name = models.CharField('Haridorni familiyasi', max_length=50)  # register qilgan paytdagi familiyani oladi
    phone = models.CharField('Haridorni telfon raqami ', max_length=50)  # kiritsh majburiy
    created_at = models.DateTimeField('Buyurtma yaratilgan vaqti', auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey('orders.Order', models.CASCADE, related_name='items')
    count = models.PositiveIntegerField('Soni', db_default=1)
    currency = models.ForeignKey('shops.Currency', models.RESTRICT)
    product_attribute = models.ForeignKey('shops.AttributeVariant', models.CASCADE, related_name='order_items')


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
        unique_together = [
            ('code', 'shop')
        ]


class ShopService(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        NOT_EXISTS = 'not_exists', 'Not exists'

    shop = models.ForeignKey('shops.Shop', models.CASCADE, related_name='shop_services')
    service = models.ForeignKey('orders.Service', models.CASCADE, related_name='service_orders')
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


class ShopServiceField(models.Model):
    shop_service = models.ForeignKey('orders.ShopService', models.CASCADE)
    field = models.ForeignKey('orders.Field', models.CASCADE)
    value = models.JSONField(default=dict)


class Field(models.Model):
    class Type(models.TextChoices):
        INTEGER = 'integer', 'Integer'
        STRING = 'string', 'String'
        TEXT = 'text', 'Text'
        LIST = 'list', 'List'
        VIDEO = 'video', 'Video'
        IMAGE = 'image', 'Image'
        GEOLOCATION = 'geolocation', 'Geolocation'

    service = models.ForeignKey('orders.Service', models.CASCADE, related_name='fields')
    label = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    max_length = models.IntegerField()
    required = models.BooleanField()
    type = models.CharField(max_length=255, choices=Type.choices)
    provider_labels = models.JSONField(null=True, blank=True)