from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Code
from .forms import OpenAIForm

class FirstAppViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testaccount', password='testadmin')

    def test_home_view(self):
        self.client.login(username='testaccount', password='testadmin')
        response = self.client.post(reverse('home'), {'user_request': 'test request', 'language_selection': 'python'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_custom_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testaccount', 'password': 'testadmin'})
        self.assertEqual(response.status_code, 302)

    def test_sign_up_view(self):
        response = self.client.post(reverse('register'), {'first_name':'testuser', 'email':'testemail@gmail.com', 'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)

    def test_past_code_view(self):
        self.client.login(username='testaccount', password='testadmin')
        response = self.client.get(reverse('past_code'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'past.html')

    def test_delete_code_view(self):
        self.client.login(username='testaccount', password='testadmin')
        code = Code.objects.create(user=self.user, question='test question', code_response='test code', language='python')
        response = self.client.post(reverse('delete_snippet', args=[code.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Code.objects.filter(pk=code.pk).exists())