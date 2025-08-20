import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Status
from django.contrib.messages import get_messages


class StatusCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123'
        )
        self.status = Status.objects.create(name='Новый статус')
        self.status_list_url = reverse('status_list')
        self.status_create_url = reverse('status_create')
        self.status_update_url = reverse(
            'status_update',
            kwargs={'pk': self.status.pk}
        )
        self.status_delete_url = reverse(
            'status_delete',
            kwargs={'pk': self.status.pk}
        )
        self.index_url = reverse('index')

    def test_status_list_view(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.get(self.status_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/status_list.html')
        self.assertContains(response, 'Новый статус')

    def test_status_list_unauthorized(self):
        response = self.client.get(self.status_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_status_create_success(self):
        self.client.login(username='testuser', password='TestPass123')
        form_data = {'name': 'В работе'}
        response = self.client.post(self.status_create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.status_list_url)
        self.assertTrue(Status.objects.filter(name='В работе').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно создан', str(messages[0]))

    def test_status_create_unauthorized(self):
        form_data = {'name': 'В работе'}
        response = self.client.post(self.status_create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_status_update_success(self):
        self.client.login(username='testuser', password='TestPass123')
        form_data = {'name': 'Обновленный статус'}
        response = self.client.post(self.status_update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.status_list_url)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Обновленный статус')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно обновлен', str(messages[0]))

    def test_status_update_unauthorized(self):
        form_data = {'name': 'Обновленный статус'}
        response = self.client.post(self.status_update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_status_delete_success(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.post(self.status_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.status_list_url)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно удален', str(messages[0]))

    def test_status_delete_unauthorized(self):
        response = self.client.post(self.status_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    # def test_status_delete_with_task(self):
    #     self.client.login(username='testuser', password='TestPass123')
    #     from task_manager.models import Task
    #     Task.objects.create(name='Тестовая задача', status=self.status)
    #     response = self.client.post(self.status_delete_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(
    #         response,
    #         'Нельзя удалить статус, связанный с задачами'
    #     )
    #     self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())


if __name__ == '__main__':
    unittest.main()
