from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['material']


class PhotoAdmin(admin.TabularInline):
    list_display = ['product']
    model = Photo


class ReviewAdmin(admin.TabularInline):
    list_display = ['user']
    model = Review

 
@admin.register(Brand)
class BrandtAdmin(admin.ModelAdmin):
    list_display = ['brand']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_img', 'name', 'created']
    exclude = ['created']
    inlines = [PhotoAdmin, ReviewAdmin]

    def get_img(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width=150 height=150>')
