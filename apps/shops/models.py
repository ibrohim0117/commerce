from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db import models

from apps.shared.django.models import CreatedBaseModel


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

    is_popular_products_show = models.BooleanField("'Ommabop mahsulotlar' sahifasini ko'rsatish", default=False,
                                            db_default=False)
    attachments = GenericRelation('shops.Attachment', blank=True)
    shop_logo = GenericRelation('shops.Attachment', blank=True)
    favicon_image = GenericRelation('shops.Attachment', blank=True)
    slider_images = GenericRelation('shops.Attachment', blank=True)

    class TemplateColor(models.Model):  # ✅
        name = models.CharField(max_length=55, verbose_name='Nomi')
        color = models.CharField(max_length=55, verbose_name='Rangi')

        class Meta:
            verbose_name = 'Shablon rangi'
            verbose_name_plural = 'Shablon ranglari'

        def __str__(self):
            return self.name


class TelegramChanel(models.Model):
    chat = models.CharField(max_length=255, unique=True, verbose_name='Telegram kanal username')
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='channels')

    class Meta:
        verbose_name = 'Telegram kanal'
        verbose_name_plural = 'Telegram kanallar'

    def __str__(self):
        return f'{self.chat}'


class ChanelMessage(models.Model):
    class FileType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        TEXT = 'text', 'Text'

    class MessageStatus(models.TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = models.CharField(max_length=4100)
    chat = models.ForeignKey(TelegramChanel, on_delete=models.CASCADE)
    is_scheduled = models.BooleanField(default=False)
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="Keyinroq jo'natish vaqti")
    file_type = models.CharField(max_length=255, choices=FileType.choices, default=FileType.TEXT)
    status = models.CharField(max_length=255, choices=MessageStatus.choices, db_default=MessageStatus.PENDING,
                              verbose_name="Habarning statusi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Xabar yaratilgan vaqti')

    class Meta:
        verbose_name = 'Telegram Kanal xabari'
        verbose_name_plural = 'Telegram kanal xabarlari'

    def __str__(self):
        return f"{self.id}. Message of {self.chat.chat}"


class ChatMessage(models.Model):
    class Type(models.TextChoices):
        USER = 'user', 'User'
        OWNER = 'owner', 'Owner'

    class ContentType(models.TextChoices):
        TEXT = 'text', 'Text'

    message = models.CharField('Xabar', max_length=4100)
    content_type = models.CharField(max_length=10, choices=Type.choices)
    seen = models.BooleanField(db_default=False)
    created_at = models.DateTimeField('Yaratilgan vaqti', auto_now_add=True)


class BroadCastMessage(models.Model):
    class MessageStatus(models.TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = models.CharField(max_length=4100, verbose_name="Habar")
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)
    is_scheduled = models.BooleanField(default=False)
    lon = models.FloatField(blank=True, null=True, verbose_name="Lokatsiya lon")
    lat = models.FloatField(blank=True, null=True, verbose_name="Lokatsiya lat")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="Keyinroq jo'natish vaqti")
    received_users = models.IntegerField(default=0, verbose_name='Qabul qiluvchilar soni')
    status = models.CharField(max_length=20, choices=MessageStatus.choices, db_default=MessageStatus.PENDING,
                       verbose_name='Xabarning statusi')
    attachments = GenericRelation('shops.Attachment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan sana')

    class Meta:
        verbose_name = 'Axborotnoma'
        verbose_name_plural = 'Axborotnomalar'


class Commerce(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = models.CharField(max_length=255, verbose_name="Domen nomi")
    status = models.CharField(max_length=8, choices=Status.choices, verbose_name="Sayt aktiv yoki aktiv emasligi")
    template_color = models.ForeignKey('shops.TemplateColor', on_delete=models.CASCADE, related_name='sites')
    is_configured = models.BooleanField(db_default=True)
    is_sub_domain = models.BooleanField(db_default=True, verbose_name='Sayt domen quygan yoki yuqligi')
    shop = models.OneToOneField('shops.Shop', models.CASCADE, related_name='sites')


class TelegramBot(models.Model):
    username = models.CharField(max_length=255, unique=True, verbose_name='Telegram username')
    token = models.CharField(max_length=255, unique=True, verbose_name='Telegram token')
    group_access_token = models.CharField(max_length=255, unique=True, verbose_name='guruhda ishlashi uchun token')
    is_new_template = models.BooleanField(verbose_name='web app True odiiy bot False')
    order_button_url = models.CharField(max_length=255)
    shop = models.OneToOneField('shops.Shop', models.CASCADE, related_name='telegram_bots')


class Category(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    name = models.CharField(max_length=255)
    emoji = models.CharField(max_length=25, blank=True, null=True)
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True, related_name='children')
    show_in_ecommerce = models.BooleanField(db_default=False)
    status = models.CharField(max_length=15, choices=Status.choices, db_default=Status.INACTIVE)
    description = models.TextField(blank=True, null=True)
    position = models.IntegerField(default=1)
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='categories')
    attachments = GenericRelation('shops.Attachment', blank=True)


class Weight(models.Model):
    name = models.CharField(max_length=10)


class Length(models.Model):
    name = models.CharField(max_length=10)


class Product(models.Model):
    class StockStatus(models.TextChoices):
        FIXED = 'fixed', 'Fixed'
        INDEFINITE = 'indefinite', 'Indefinite'
        NOT_AVAILABLE = 'not_available', 'Not available'

    class Unit(models.TextChoices):
        ITEM = 'item', 'Item'
        WEIGHT = 'weight', 'Weight'

    name = models.CharField(max_length=255, verbose_name='Mahsulot nomi')
    category = models.ForeignKey('shops.Category', on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Sotuv narxi')
    full_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Umumiy narxi')
    description = models.TextField()
    has_available = models.BooleanField(db_default=True, verbose_name='Mahsulotni yoqish yoki uchirish')

    weight = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)

    ikpu_code = models.IntegerField(null=True, blank=True, verbose_name='IKPU kod')
    package_code = models.IntegerField(null=True, blank=True, verbose_name='qadoq kodi')
    stock_status = models.CharField(max_length=100, choices=StockStatus.choices)
    quantity = models.IntegerField(db_default=0, verbose_name='product soni status indefinite bulganda chiqadi')
    barcode = models.IntegerField(null=True, blank=True, verbose_name='Barkod')
    vat_percent = models.IntegerField(db_default=0, verbose_name='QQS foizi')
    position = models.IntegerField(db_default=1, verbose_name='sort order')
    internal_notes = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=20, choices=Unit.choices)
    weight_class = models.ForeignKey('shops.Weight', models.CASCADE, related_name='weights')
    length_class = models.ForeignKey('shops.Length', models.CASCADE, related_name='lengths')
    attachments = GenericRelation('shops.Attachment', blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(full_price__gte=models.F('price')), name='check_full_price')
        ]


class Attachment(CreatedBaseModel):
    content_type = models.ForeignKey('contenttypes.ContentType', models.CASCADE, null=True, blank=True, related_name='attachments')
    record_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'record_id')
    key = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)


class Attribute(models.Model):  # ✅
    name = models.CharField(max_length=50)
    product = models.ForeignKey('shops.Product', models.CASCADE, related_name='attributes')


class AttributeValue(models.Model):  # ✅
    value = models.CharField(max_length=20)
    attribute = models.ForeignKey('shops.Attribute', models.CASCADE, related_name='values')


class AttributeVariant(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sotuv narxi')
    full_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Umumiy narx')
    weight_class = models.ForeignKey('shops.Weight', models.CASCADE, blank=True, null=True, related_name='weights')
    length_class_id = models.ForeignKey('shops.Length', models.CASCADE, blank=True, null=True, related_name='lengths')
    weight = models.IntegerField(null=True, blank=True, verbose_name='Vazni')
    length = models.IntegerField(null=True, blank=True, verbose_name='Uzunligi')
    height = models.IntegerField(null=True, blank=True, verbose_name='Balandligi')
    width = models.IntegerField(null=True, blank=True, verbose_name='Kengligi')
    package_code = models.IntegerField(null=True, blank=True)
    ikpu_code = models.IntegerField(null=True, blank=True)
    stock_status = models.CharField(max_length=20)
    quantity = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=20)
    barcode = models.IntegerField(null=True, blank=True)
    has_available = models.BooleanField(db_default=False)
    vat_percent = models.IntegerField(db_default=0)
    product = models.ForeignKey('shops.Product', models.CASCADE, related_name='variants')


