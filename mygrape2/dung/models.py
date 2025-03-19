from django.db import models

# from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from accounts.models import CustomUser
# Create your models here.

class Dung(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=False, db_index=True, verbose_name='Наименование')
    alias = models.CharField(max_length=100, verbose_name='Синоним')
    description = tinymce_models.HTMLField(verbose_name='Описание')

    def __str__(self):
        return self.name


class JornalDung(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=False, db_index=True, verbose_name='Наименование')
    alias = models.CharField(max_length=200, blank=True, null=True, verbose_name='Синоним')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    userid = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    def __str__(self):
        return f"{self.name} в наличии {self.quantity} г"