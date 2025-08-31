import unittest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.models import Task, Status, Label
from django.contrib.messages import get_messages


class FilterCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='TestPass123')
        self.user2 = User.objects.create_user(username='testuser2', password='TestPass123')
        self.status = Status.objects.create(name='Новый статус')
        self.label = Label.objects.create(name='Bug')
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

    def test_task_filter_by_status(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url, {'status': str(self.status.pk)})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)

    def test_task_filter_by_assignee(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url, {'assignee': str(self.user2.pk)})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task1)

    def test_task_filter_by_labels(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url, {'labels': str(self.label.pk)})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task1)
        self.assertIn(self.label, tasks[0].labels.all())
        print(f"Filtered tasks (labels): {tasks}")

    def test_task_filter_by_own_tasks(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url, {'own_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task1)
        print(f"Filtered tasks (own_tasks): {tasks}")

    def test_task_filter_no_params(self):
        self.client.login(username='testuser1', password='TestPass123')
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)  # Ожидаем все задачи без фильтров
        print(f"Tasks with no params: {tasks}")

    def test_task_filter_unauthorized(self):
        response = self.client.get(self.task_list_url, {'status': str(self.status.pk)})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))


if __name__ == '__main__':
    unittest.main()
