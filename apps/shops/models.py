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


class BroadCastMessage(models.Model):
    class MessageStatus(models.TextChoices):
        SENT = 'sent', 'Sent'
        PENDING = 'pending', 'Pending'
        NOT_SENT = 'not_sent', 'Not sent'

    message = models.CharField(max_length=4100, verbose_name="Habar")
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE)
    lon = models.FloatField(blank=True, null=True, verbose_name="Lokatsiya lon")
    lat = models.FloatField(blank=True, null=True, verbose_name="Lokatsiya lat")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="Keyinroq jo'natish vaqti")
    received_users = models.IntegerField(default=0, verbose_name='Qabul qiluvchilar soni')
    status = models.CharField(max_length=20, choices=MessageStatus.choices, db_default=MessageStatus.PENDING,
                       verbose_name='Xabarning statusi')
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






