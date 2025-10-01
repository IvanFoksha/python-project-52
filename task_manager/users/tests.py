import unittest
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from django.contrib.messages import get_messages


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123',
            first_name='Test',
            last_name='User'
        )
        self.create_url = reverse('user_create')
        self.update_url = reverse('user_update', kwargs={'pk': self.user.pk})
        self.delete_url = reverse('user_delete', kwargs={'pk': self.user.pk})
        self.list_url = reverse('user_list')
        self.user_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'NewPass123',
            'password2': 'NewPass123'
        }

    def test_create_user_success(self):
        """Test successful user creation."""
        response = self.client.post(
            reverse('user_create'),
            self.user_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            User.objects.filter(username=self.user_data['username']).exists()
        )
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            'Пользователь успешно зарегистрирован'
        )
        self.assertRedirects(response, reverse('login'))

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
        self.assertContains(
            response,
            'Пароль должен содержать минимум 8 символов'
        )

    def test_create_user_password_mismatch(self):
        form_data = {
            'username': 'mismatchuser',
            'first_name': 'Mismatch',
            'last_name': 'User',
            'password1': 'NewPass123',
            'password2': 'DifferentPass123'
        }
        response = self.client.post(self.create_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())
        self.assertContains(response, 'Пароли не совпадают')

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
        self.assertRedirects(response, self.list_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_update_user_no_password_change(self):
        """Test updating user data without changing the password."""
        self.client.force_login(self.user)
        updated_data = {
            'username': 'new_testuser',
            'first_name': 'New',
            'last_name': 'User',
            'password': ''
        }
        response = self.client.post(
            reverse('user_update', args=[self.user.pk]),
            updated_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, 'new_testuser')
        self.assertEqual(updated_user.first_name, 'New')
        self.assertEqual(updated_user.last_name, 'User')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('Пользователь успешно изменен', str(messages[0]))
        self.assertRedirects(response, reverse('user_list'))

    def test_update_user_unauthorized(self):
        another_user = User.objects.create_user(
            username='anotheruser',
            password='AnotherPass123',
            first_name='Another',
            last_name='User'
        )
        self.client.login(username='testuser', password='TestPass123')
        update_url = reverse('user_update', kwargs={'pk': another_user.pk})
        response = self.client.post(update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('У вас нет прав для редактирования', str(messages[0]))

    def test_update_user_unauthenticated(self):
        form_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'UpdatedPass123',
            'password2': 'UpdatedPass123'
        }
        response = self.client.post(self.update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('TestPass123'))

    def test_delete_user_success(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertRedirects(response, self.list_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')

    def test_delete_user_unauthorized(self):
        """Test deleting a user by another unauthorized user."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('user_delete', args=[self.user.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')
        self.assertRedirects(response, reverse('user_list'))

    def test_delete_user_unauthenticated(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/')
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())


if __name__ == '__main__':
    unittest.main()
