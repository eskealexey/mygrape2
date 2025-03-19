from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import User

from tinymce import models as tinymce_models
from accounts.models import CustomUser
from sickpest.models import SickPest

class Preparats(models.Model):
    TYPES_CHOICES = (
        ('0', 'Акарициды'),
        ('1', 'Фунгициды'),
        ('2', 'Гербициды'),
        ('3', 'Арборициды'),
        ('4', 'Нематициды'),
        ('5', 'Родентициды'),
        ('6', 'Пестициды')
    )

    ACTIONS_CHOICES = (
        ('0', 'Системный'),
        ('1', 'Контактный'),
        ('2', 'Контактно-проникающий'),
        ('3', 'Биопрепарат'),
    )


    name = models.CharField(max_length=100, verbose_name='Наименование')
    sick_id = models.ManyToManyField(SickPest, verbose_name='Болезни')
    action = models.CharField(max_length=1, choices=ACTIONS_CHOICES, default='0', verbose_name='Действие')
    srok_og = models.CharField(max_length=100, verbose_name='Срок ожидания')
    srok_zaq = models.CharField(max_length=100, verbose_name='Срок защиты')
    type_preparat = CharField(max_length=1, choices=TYPES_CHOICES, default='1', verbose_name='Тип препарата')
    description = tinymce_models.HTMLField(verbose_name='Описание')

    def __str__(self):
        return self.name

class JornalPreparat(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=False, db_index=True, verbose_name='Наименование')
    alias = models.CharField(max_length=200, blank=True, null=True, verbose_name='Синоним')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    userid = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.name} в наличии {self.quantity} г"