from django.test import TestCase
from django.urls import reverse

from .forms import ContactsForm, Contacts


class TestHomeView(TestCase):
    def test_get(self):

        response = self.client.get(reverse('company:Home'))

        self.assertEqual(response.status_code, 200)


class TestContactsView(TestCase):
    def test_get(self):

        response = self.client.get(reverse('company:Contacts'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ContactsForm)

    def test_post(self):

        data = {
            'email': 'test@gmail.com',
            'full_name': 'Someone'
        }
        response = self.client.post(reverse('company:Contacts'), data=data)

        self.assertEqual(response.status_code, 302)

        contact = Contacts.objects.get(pk=1)

        self.assertEqual(contact.email, data['email'])

    def test_form_errors(self):

        data = {
            'full_name': 'Someone'
        }

        response = self.client.post(reverse('company:Contacts'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context['form'].errors)







