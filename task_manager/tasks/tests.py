import unittest
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.messages import get_messages


class TaskTests(TestCase):
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
        self.another_user = User.objects.create_user(
            username='anotheruser',
            password='AnotherPassword123'
        )
        self.status = Status.objects.create(name='Test Status')
        self.label = Label.objects.create(name='Test Label')
        self.task1 = Task.objects.create(
            name='Тестовая задача 1',
            description='Описание 1',
            status=self.status,
            author=self.user1,
            assignee=self.user2
        )
        self.task1.labels.add(self.label)
        self.task2 = Task.objects.create(
            name='Тестовая задача 2',
            description='Описание 2',
            status=self.status,
            author=self.user2
        )
        self.task_list_url = reverse('task_list')
        self.task_create_url = reverse('task_create')
        self.task_detail_url = reverse(
            'task_detail',
            kwargs={'pk': self.task1.pk}
        )
        self.task_update_url = reverse(
            'task_update',
            kwargs={'pk': self.task1.pk}
        )
        self.task_delete_url = reverse(
            'task_delete',
            kwargs={'pk': self.task1.pk}
        )

    # CRUD тесты
    def test_task_list_view(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Тестовая задача 1')
        self.assertContains(response, 'Тестовая задача 2')

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
            'assignee': self.user2.pk,
            'labels': [self.label.pk]
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
            'assignee': self.user2.pk,
            'labels': [self.label.pk]
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
        self.assertContains(response, 'Тестовая задача 1')

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
            'assignee': self.user2.pk,
            'labels': [self.label.pk]
        }
        response = self.client.post(self.task_update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'Обновленная задача')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Задача успешно изменена', str(messages[0]))

    def test_task_update_unauthorized(self):
        """Test updating a task by an unauthorized user."""
        self.client.logout()
        response = self.client.post(
            reverse('task_update', args=[self.task1.pk]),
            {
                'name': 'Обновленная задача',
                'description': 'Новое описание',
                'status': self.status.pk,
                'executor': self.user2.pk,
                'labels': [self.label.pk]
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            'У вас нет прав для изменения этой задачи.',
            str(messages[0])
        )
        self.assertRedirects(response, reverse('index'))

    def test_task_delete_success(self):
        """Test successful task deletion."""
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())
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
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse('task_delete', args=[self.task1.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn(
            'Задачу может удалить только ее автор.',
            str(messages[0])
        )
        self.assertRedirects(response, reverse('task_list'))

    # Тесты фильтров
    def test_task_filter_by_status(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(
            self.task_list_url,
            {'status': str(self.status.pk)}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)

    def test_task_filter_by_assignee(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(
            self.task_list_url,
            {'assignee': str(self.user2.pk)}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task1)

    def test_task_filter_by_labels(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(
            self.task_list_url,
            {'labels': [str(self.label.pk)]}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task1)
        self.assertIn(self.label, tasks[0].labels.all())

    def test_task_filter_by_own_tasks(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url, {'own_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task1)

    def test_task_filter_no_params(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)

    def test_task_filter_unauthorized(self):
        response = self.client.get(
            self.task_list_url,
            {'status': str(self.status.pk)}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))


if __name__ == '__main__':
    unittest.main()
