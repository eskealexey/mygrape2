from django.db import models

from tinymce import models as tinymce_models


class SickPest(models.Model):
    TYPE_CHOICES = [
        ('0', 'вредитель'),
        ('1', 'болезнь'),
        ('2', 'стресс'),
    ]

    name = models.CharField(max_length=150, verbose_name='Название')
    type_s = models.CharField(max_length=1, choices=TYPE_CHOICES, default='1', verbose_name='Тип')
    description = tinymce_models.HTMLField(verbose_name='Описание')

    def __str__(self):
        return self.name


class SickPestImage(models.Model):
    image = models.ImageField(upload_to='sickpest/images', null=True, blank=True, verbose_name='Изображение')
    sickpest = models.ForeignKey(SickPest, on_delete=models.CASCADE,null=True, blank=True,verbose_name='Болезнь')

    def __str__(self):
        return self.image.name