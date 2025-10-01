import unittest
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.contrib.messages import get_messages
from task_manager.users.models import User


class StatusTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123'
        )
        self.status = Status.objects.create(name='Новый статус')
        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание задачи',
            status=self.status,
            author=self.user
        )
        self.label = Label.objects.create(name='Тестовая метка')
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
        status = Status.objects.create(name='Удаляемый статус')
        delete_url = reverse('status_delete', kwargs={'pk': status.pk})
        response = self.client.post(delete_url, {'confirm': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.status_list_url)
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно удален', str(messages[0]))

    def test_status_delete_with_task(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.post(self.status_delete_url, {'confirm': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.status_list_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(
            'Нельзя удалить статус, связанный с задачами',
            str(messages[0])
        )
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_delete_unauthorized(self):
        response = self.client.post(self.status_delete_url, {'confirm': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())


if __name__ == '__main__':
    unittest.main()