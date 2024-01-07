from django.db import models


class Contacts(models.Model):
    full_name = models.CharField(verbose_name='Full name', max_length=25, unique=True)
    email = models.EmailField(verbose_name='Email')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'Contacts'
