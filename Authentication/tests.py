from django.test import TestCase, Client
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User

class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            "email": "test@gmail.com",
            'password1': 'test123',
            'password2': 'test123'
        })
        self.assertEqual(response.status_code, 302)  # Redirected after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())  # User object created

    def test_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': "test@gmail.com",
            'password1': 'test123',
            'password2': 'test123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'email': "test@gmail.com",
            'password1': 'test123',
            'password2': 'invalidpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='test123')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 302)  # Redirected after successful login

    def test_login_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'test123'
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {
            'username': 'testuser',
            'password': 'invalidpassword'
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

