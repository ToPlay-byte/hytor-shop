from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(read_only=True, slug_field='material', many=True)
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='brand', read_only=True)
    category = serializers.SlugRelatedField(slug_field='category', read_only=True, many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

