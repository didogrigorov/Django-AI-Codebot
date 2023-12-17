from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from website.models import Code
from website.forms import OpenAIForm, SignUpForm


class UserFormTest(TestCase):

    def test_signup_form_valid(self):
        form_data = {
            'first_name': 'testuser',
            'last_name': 'testuser123',
            'email': 'testemail@gmail.com',
            'username': 'newuser',
            'password1': 'newpassword@#',
            'password2': 'newpassword@#'
        }
        form = SignUpForm(form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form_data = {
            'first_name': 'testuser',
            'email': 'testemail@gmail.com',
            'username': 'newuser',
            'password1': 'newpassword@#',
            'password2': 'newpassword@#'
        }
        form = SignUpForm(form_data)

        self.assertIn("last_name", form.errors)
        self.assertFalse(form.is_valid())

    def test_signup_form_email_field_invalid(self):
        form_data = {
            'first_name': 'testuser',
            'email': 'testemailgmail.com',
            'last_name': 'testuser123',
            'username': 'newuser',
            'password1': 'newpassword@#',
            'password2': 'newpassword@#'
        }
        form = SignUpForm(form_data)

        self.assertIn("email", form.errors)
        self.assertFalse(form.is_valid())


class OpenAIFormTest(TestCase):
    def test_openai_valid(self):
        form_data = {
            'user_request': "Write me a counter from 1 to 10",
            'language_selection': 'Python'
        }
        form = OpenAIForm(form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_openai_invalid(self):
        form_data = {
            'user_request': "",
            'language_selection': 'Python'
        }
        form = OpenAIForm(form_data)
        self.assertIn("user_request", form.errors)
        self.assertIn("This field is required.", form.errors["user_request"])
        self.assertFalse(form.is_valid())


