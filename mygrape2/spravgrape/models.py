from django.db import models
from tinymce.models import HTMLField


# from tinymce import models as tinymce_models

# Create your models here.
class SortGrape(models.Model):
    NAZNACH_CHOICES = [
        ('ST', 'столовый'),
        ('KM', 'кишмиш'),
        ('TN', 'технический'),
        ('UN', 'универсальный'),
    ]
    SORT_CHOICES = [
        ('0', 'Сорт'),
        ('1', 'Гибридная форма'),
    ]
    VKUS_CHOICES = [
        ('0', 'Гармоничный'),
        ('1', 'Мускатный'),
        ('2', 'Простой'),
        ('3', 'Фруктовый'),
    ]
    TYPE_CHOICES = [
        ('O', 'обоеполый'),
        ('Q', 'женский'),
    ]

    name = models.CharField(max_length=100, blank=False, unique=False, db_index=True, verbose_name='название')
    alias = models.CharField(max_length=255, blank=True, verbose_name='синоним')
    naznacn = models.CharField(max_length=2, choices=NAZNACH_CHOICES, default='ST', verbose_name='назначение')
    authors = models.CharField(max_length=255, default='-', verbose_name='авторы')
    parents = models.CharField(max_length=255, default='-', verbose_name='родители')
    sortnost = models.CharField(max_length=1, choices=SORT_CHOICES, default='1', verbose_name='сортность')
    gr_forma = models.CharField(max_length=50, blank=True, default='-', verbose_name='форма грозди')
    gr_plotnost = models.CharField(max_length=50, blank=True, default='-', verbose_name='плотность грозди')
    gr_ves = models.CharField(max_length=10, blank=True, default='-', verbose_name='вес грозди')
    br_color = models.CharField(max_length=50, blank=True, default='-', verbose_name='цвет_ягоды')
    br_vkus = models.CharField(max_length=1, blank=True, choices=VKUS_CHOICES, default='0', verbose_name='вкус ягоды')
    brix = models.CharField(max_length=3, blank=True, default='-', verbose_name='brix')
    br_forma = models.CharField(max_length=25, blank=True, verbose_name='форма ягоды')
    br_ves = models.CharField(max_length=8, blank=True, default='-', verbose_name='вес ягоды')
    br_size = models.CharField(max_length=10, blank=True, default='-', verbose_name='размер ягоды')
    frozen_re = models.CharField(max_length=4, blank=True, verbose_name='морозостойкость')
    type_fl = models.CharField(max_length=20, choices=TYPE_CHOICES, default='O', verbose_name='тип цветка')
    rost = models.CharField(max_length=25, blank=True, verbose_name='сила роста')
    obrezka = models.CharField(max_length=150, blank=True, verbose_name='обрезка')
    srok_day = models.CharField(max_length=10, blank=True, verbose_name='срок(в днях)')
    srok = models.CharField(max_length=25, blank=True, verbose_name='срок')
    img_url = models.ImageField(verbose_name='изображение', upload_to='sorts/foto', default=None, blank=True)

    def __str__(self):
        return self.name


class InfoGrape(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name='название')
    article = HTMLField(blank=True, verbose_name='текст')
    id_sort = models.ForeignKey(SortGrape, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

