# Generated by Django 4.2.6 on 2023-10-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_order_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='active',
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total price'),
        ),
    ]
