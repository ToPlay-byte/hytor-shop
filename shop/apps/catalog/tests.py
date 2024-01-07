from django.test import TestCase, Client
from django.urls import reverse


class TestDetailToy(TestCase):
    def setUp(self):
        self.client = Client()

    def test_detail(self):
        response = self.client.get(reverse('catalog:toy', kwargs={'name': 'The bear'}))
        self.assertEqual(response.status_code, 200)




