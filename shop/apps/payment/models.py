from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.catalog.models import Product


class Order(models.Model):

    first_name = models.CharField(verbose_name='First name', max_length=16)
    last_name = models.CharField(verbose_name='Last name', max_length=16)
    email = models.EmailField(verbose_name='Email')
    product = models.ForeignKey(Product, verbose_name="Toy's name", on_delete=models.CASCADE)
    created = models.DateField(verbose_name='Created', default=timezone.now)
    paid = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Quantity', default=1)
    total_price = models.DecimalField(verbose_name='Total price', decimal_places=2, max_digits=10)

    def save(self, *args, **kwargs):
        Product.objects.filter(name=self.product.name).update(quantity=models.F('quantity') - self.quantity)
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        Product.objects.filter(name=self.product.name).update(quantity=models.F('quantity') + self.quantity)
        return super().delete(using, keep_parents)

    def __str__(self):
        return f'{self.user}, {self.product}'





        
        
