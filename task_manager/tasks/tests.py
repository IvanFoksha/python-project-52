import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Task, Status
from django.contrib.messages import get_messages


class TaskCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='TestPass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='TestPass123'
        )
        self.status = Status.objects.create(name='Новый статус')
        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание задачи',
            status=self.status,
            author=self.user1,
            assignee=self.user2
        )
        self.task_list_url = reverse('task_list')
        self.task_create_url = reverse('task_create')
        self.task_detail_url = reverse(
            'task_detail',
            kwargs={'pk': self.task.pk}
        )
        self.task_update_url = reverse(
            'task_update',
            kwargs={'pk': self.task.pk}
        )
        self.task_delete_url = reverse(
            'task_delete',
            kwargs={'pk': self.task.pk}
        )

    def test_task_list_view(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Тестовая задача')

    def test_task_list_unauthorized(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_task_create_success(self):
        self.client.login(username='testuser1', password='TestPass123')
        form_data = {
            'name': 'Новая задача',
            'description': 'Новое описание',
            'status': self.status.pk,
            'assignee': self.user2.pk
        }
        response = self.client.post(self.task_create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно создана', str(messages[0]))

    def test_task_create_unauthorized(self):
        form_data = {
            'name': 'Новая задача',
            'description': 'Новое описание',
            'status': self.status.pk,
            'assignee': self.user2.pk
        }
        response = self.client.post(self.task_create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_task_detail_view(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, 'Тестовая задача')

    def test_task_detail_unauthorized(self):
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_task_update_success(self):
        self.client.login(username='testuser1', password='TestPass123')
        form_data = {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': self.status.pk,
            'assignee': self.user2.pk
        }
        response = self.client.post(self.task_update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновленная задача')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно обновлена', str(messages[0]))

    def test_task_update_unauthorized(self):
        form_data = {
            'name': 'Обновленная задача',
            'description': 'Новое описание',
            'status': self.status.pk,
            'assignee': self.user2.pk
        }
        response = self.client.post(self.task_update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_task_delete_success(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно удалена', str(messages[0]))

    def test_task_delete_unauthorized(self):
        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_task_delete_not_author(self):
        self.client.login(username='testuser2', password='TestPass123')
        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(
            'Удаление задачи может выполнить только автор.',
            str(messages[0])
        )
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())


if __name__ == '__main__':
    unittest.main()
