from django.test import TestCase
from django.urls import reverse

from .forms import ReviewForm
from .models import (
    Review, Product,
    Category, Brand,
    Material
)


class TestProduct(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category='electro')
        self.brand = Brand.objects.create(brand='fasdfas')
        self.material = Material.objects.create(material='plastic')

        self.product = Product.objects.create(id=2, name='The bear', description='sdfa', brand=self.brand)

        self.product.category.add(self.category)
        self.product.material.add(self.material)

    def test_detail(self):

        response = self.client.get(reverse('catalog:toy', kwargs={'name': 'The bear'}))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['toy'], Product)


class TestCatalogView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category='electro')
        self.brand = Brand.objects.create(brand='fasdfas')
        self.material = Material.objects.create(material='plastic')

        self.product = Product.objects.create(id=2, name='The bear', description='sdfa', brand=self.brand)

        self.product.category.add(self.category)
        self.product.material.add(self.material)

    def test_get(self):

        response = self.client.get(reverse('catalog:main'))

        self.assertEqual(response.status_code, 200)

    def test_selected_category(self):

        response = self.client.get(reverse('catalog:category', kwargs={'category': 'electro'}))
        data = response.context['products']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data)

    def test_search(self):

        response = self.client.get(reverse('catalog:search'), {'query': 'The bear'})
        data = response.context['products']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data)

















