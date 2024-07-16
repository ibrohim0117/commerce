from django.db import models

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
