import unittest
from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password


class UserCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            password=make_password('TestPass123'),
            first_name='Test',
            last_name='User'
        )
        self.create_url = reverse('user_create')
        self.update_url = reverse('user_update', kwargs={'pk': self.user.pk})
        self.delete_url = reverse('user_delete', kwargs={'pk': self.user.pk})

    def test_create_user_success(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'NewPass123',
            'password2': 'NewPass123'
        }
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно создан', str(messages[0]))

    def test_create_user_invalid_password(self):
        form_data = {
            'username': 'invaliduser',
            'first_name': 'Invalid',
            'last_name': 'User',
            'password1': 'short',
            'password2': 'short'
        }
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='invaliduser').exists())
        self.assertContains(response, 'Пароль должен содержать минимум 8 символов')

    def test_update_user_success(self):
        self.client.login(username='testuser', password='TestPass123')
        form_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'UpdatedPass123',
            'password2': 'UpdatedPass123'
        }
        response = self.client.post(self.update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertTrue(self.user.check_password('UpdatedPass123'))
        self.assertRedirects(response, reverse('user_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно обновлен', str(messages[0]))

    def test_update_user_unauthorized(self):
        self.client.login(username='testuser', password='TestPass123')
        another_user = User.objects.create_user(
            username='anotheruser',
            password=make_password('AnotherPass123'),
            first_name='Another',
            last_name='User'
        )
        update_url = reverse('user_update', kwargs={'pk': another_user.pk})
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))

    def test_delete_user_succsess(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertRedirects(response, reverse('user_list'))

    def test_delete_user_unauthorized(self):
        another_user = User.objects.create_user(
            username='anotheruser',
            password=make_password('AnotherPass123'),
            first_name='Another',
            last_name='User'
        )
        delete_url = reverse('user_delete', kwargs={'pk': another_user.pk})
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user_list'))
        self.assertTrue(User.objects.filter(pk=another_user.pk).exists())


if __name__ == '__main__':
    unittest.main()
