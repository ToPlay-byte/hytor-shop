import os

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone


def get_poster_path(obj, filename):
    """Ця функція повертає шлях до папки з постерами до продукту

    Параметри:
        obj: клас моделі
        filename: назва файлу
    """

    return os.path.join('catalog', str(obj.name), filename)


def get_photos_path(obj, filename):
    """Ця функція повертає шлях до папки з фотографіями до продукту

    Параметри:
        obj: клас моделі
        filename: назва файлу
    """

    return os.path.join('catalog', str(obj.product.name), filename)


class Product(models.Model):
    """Зберігає усю інформацію про товар"""

    name = models.CharField(verbose_name='Name', max_length=40, db_index=True, unique=True)
    description = models.CharField(verbose_name='Describe your toys', max_length=2000)
    created = models.DateField(verbose_name='Created', blank=True, default=timezone.now)
    material = models.ManyToManyField('Material', verbose_name='Materials')
    poster = models.ImageField(verbose_name='Poster', default=f'media/catalog/Unknown.png', upload_to=get_poster_path)
    brand = models.ForeignKey(
        'Brand', verbose_name='Brand', related_name='brands',
        on_delete=models.CASCADE
    )
    age = models.IntegerField(verbose_name='Age', default=0)
    quantity = models.IntegerField(verbose_name='Quantity', default=0)
    price = models.FloatField(verbose_name='Price', default=0)
    category = models.ManyToManyField('Category', verbose_name='Category', related_name='categories')
    objects = models.Manager()

    def get_id(self):
        return str(self.pk)

    def get_absolute_url(self):
        """Отримуємо точний шлях """
        return reverse('catalog:toy', kwargs={'name': self.name})

    @property
    def available(self):
        """Перевіряє чи товар в наявності"""
        return True if self.quantity else False

    def get_first_image(self):
        """Отримуємо першу фотографію"""
        return self.photos.all()[0].image.url

    def __str__(self):
        return self.name


class Category(models.Model):
    """Ця модель зберігає категорії до товару, за якими потім здійснюється пошук"""

    category = models.CharField(verbose_name='Category', max_length=25, unique=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Review(models.Model):
    """Ця модель зберігає відгуки про товар"""

    comment = models.CharField(verbose_name='Comment', max_length=256, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    review = models.ForeignKey('Product', verbose_name='Product', related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class Photo(models.Model):
    """Ця модель зберігає фотографії до товару"""

    image = models.ImageField(verbose_name='Image', upload_to=get_photos_path)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='photos')


class Brand(models.Model):
    """Ця модель зберігає бренд до товару"""

    brand = models.CharField(verbose_name='Brand', max_length=40, unique=True)

    def __str__(self):
        return self.brand


class Material(models.Model):
    """Ця модель зберігає матеріали з яких зроблений товар"""

    material = models.CharField(verbose_name='Material', max_length=16, unique=True)

    def __str__(self):
        return self.material


