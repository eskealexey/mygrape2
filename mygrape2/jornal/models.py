import os
import uuid

from django.db import models

from spravgrape.models import SortGrape
from dung.models import Dung
from preparats.models import Preparats
from tinymce import models as tinymce_models

from django.contrib.auth.models import User

from accounts.models import CustomUser


# Create your models here.

def get_dynamic_upload_path(instance, filename):
    # Получаем уникальный идентификатор для файла
    unique_id = uuid.uuid4()
    # Получаем расширение файла
    ext = filename.split('.')[-1]
    # Определяем динамическую директорию, например, по атрибуту в экземпляре
    folder_name = instance.nameuser if hasattr(instance, 'nameuser') else 'uploads'
    # Создание нового имени файла
    new_filename = f"{unique_id}.{ext}"
    # Возвращаем путь для сохранения файла
    return os.path.join(f'location/{folder_name}', new_filename)


class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name='Посадочное место')
    sort_id = models.ManyToManyField(SortGrape,blank=True, verbose_name='Сорт винограда из справочника', related_name='sorts')
    sort = models.CharField(max_length=200, blank=True, null=True, verbose_name='Сорт винограда')
    date_posadki = models.DateField(auto_now_add=False, verbose_name='Дата посадки')
    mesto = models.CharField(max_length=200, verbose_name='Местоположение')
    # mesto_graf = models.ImageField(upload_to='location/', verbose_name='Местоположение графика')
    mesto_graf = models.ImageField(upload_to=get_dynamic_upload_path, verbose_name='Местоположение графика')
    date_delete = models.DateField(auto_now_add=False, blank=True, null=True, verbose_name='Дата удаления')
    prichina = models.CharField(max_length=255, blank=True, null=True, verbose_name='Причина удаления')
    status = models.IntegerField(default=0, verbose_name='Статус')
    nameuser = models.CharField(max_length=200, blank=True, null=True, verbose_name='Имя пользователя')
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    def __str__(self):
        return self.name


class Notes(models.Model):
    title_note = models.CharField(max_length=200, verbose_name='Заголовок')
    description = tinymce_models.HTMLField(blank=True, verbose_name='Описание')
    date_add = models.DateField(auto_now_add=False, verbose_name='Дата добавления')
    locationid = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, verbose_name='Местоположение')
    def __str__(self):
        return self.title_note


class GreenOper(models.Model):
    description = tinymce_models.HTMLField(blank=True, verbose_name='Описание')
    date_add = models.DateField(auto_now_add=False, verbose_name='Дата добавления')
    locationid = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, verbose_name='Местоположение')
    def __str__(self):
        return self.locationid.name + ' ' + str(self.pk)


class Feeding(models.Model):
    dung_id = models.ManyToManyField(Dung, blank=True, verbose_name='подкормка из списка', related_name='dungs')
    dung = models.CharField(max_length=200, blank=True, null=True, verbose_name='подкормка')
    description = tinymce_models.HTMLField(blank=True, verbose_name='Описание')
    date_add = models.DateField(auto_now_add=False, verbose_name='Дата добавления')
    locationid = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, verbose_name='Местоположение')
    def __str__(self):
        return self.locationid.name + ' ' + str(self.pk)


class Processing(models.Model):
    preparat_id = models.ManyToManyField(Preparats,  blank=True, verbose_name='препарат из списка', related_name='preparats')
    preparat = models.CharField(max_length=200, blank=True, null=True, verbose_name='препарат')
    description = tinymce_models.HTMLField(blank=True, verbose_name='Описание')
    date_add = models.DateField(auto_now_add=False, verbose_name='Дата добавления')
    locationid = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, verbose_name='Местоположение')
    def __str__(self):
        return self.locationid.name + ' ' + str(self.pk)