from django.test import TestCase
from wardrobeapp.forms import UserRegisterForm

class RegisterFormTest(TestCase):
    def test_register_form_valid_data(self):
        form = UserRegisterForm(data={
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_data(self):
        form = UserRegisterForm(data={
            'username': '',
            'email': 'invalid',
            'password1': 'pass',
            'password2': 'differentpass'
        })
        self.assertFalse(form.is_valid())
