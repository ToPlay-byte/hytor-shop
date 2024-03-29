# Generated by Django 4.2.6 on 2024-01-28 21:12

import apps.catalog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=40, unique=True, verbose_name='Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=25, unique=True, verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=16, unique=True, verbose_name='Material')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=40, unique=True, verbose_name='Name')),
                ('description', models.CharField(max_length=2000, verbose_name='Describe your toys')),
                ('created', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Created')),
                ('poster', models.ImageField(default='media/catalog/Unknown.png', upload_to=apps.catalog.models.get_poster_path, verbose_name='Poster')),
                ('age', models.IntegerField(default=0, verbose_name='Age')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('price', models.FloatField(default=0, verbose_name='Price')),
                ('brand', models.ForeignKey(default=[0], on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='catalog.brand', verbose_name='Brand')),
                ('category', models.ManyToManyField(default=[0], related_name='categories', to='catalog.category', verbose_name='Category')),
                ('material', models.ManyToManyField(to='catalog.material', verbose_name='Materials')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=256, null=True, verbose_name='Comment')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='catalog.product', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.catalog.models.get_photos_path, verbose_name='Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='catalog.product')),
            ],
        ),
    ]
