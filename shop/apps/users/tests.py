from django.test import TestCase
from django.urls import reverse

from captcha.conf import settings

from .forms import SignUpForm, LoginForm, CustomUser


class TestRegistrationView(TestCase):
    def test_get(self):

        response = self.client.get(reverse('users:Sign up'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_post(self):

        data = {
            'first_name': 'John',
            'last_name': 'Unknown',
            'email': 'oleksandr.hnylosyr@gmail.com',
            'password': 'Dofasdfomdasfaoom2002',
            'sex': 'Male',
            'username': 'Hipi'

        }
        response = self.client.post(reverse('users:Sign up'), data=data)

        self.assertEqual(response.status_code, 302)

        user = CustomUser.objects.get(first_name='John')

        self.assertEqual(user.email, data['email'])

    def test_form_errors(self):

        data = {
            'first_name': 'John',
            'last_name': 'Unknown',
            'email': 'oleksandr.hnylosyr@gmail.com',
            'sex': 'Male',
            'username': 'Hipi'

        }
        response = self.client.post(reverse('users:Sign up'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('password', response.context['form'].errors)


class TestLoginView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user('toplay', 'email.oleksandr@gmail.com', 'password2131')
        from captcha.conf import settings as captcha_settings
        captcha_settings.CAPTCHA_TEST_MODE = True

    def test_get(self):

        response = self.client.get(reverse('users:Log in'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_post(self):

        data = {
            'email': 'email.oleksandr@gmail.com',
            'password': 'password2131',
            "captcha_0": "8e10ebf60c5f23fd6e6a9959853730cd69062a15",
            "captcha_1": "PASSED",
        }
        response = self.client.post(reverse('users:Log in'), data=data)

        self.assertEqual(response.status_code, 302)

    def test_form_errors(self):

        data = {
            'password': 'password2131',
            'captcha_0': '8e10ebf60c5f23fd6e6a9959853730cd69062a15',
            'captcha_1': 'PASSED',
        }
        response = self.client.post(reverse('users:Log in'), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context['form'].errors)
