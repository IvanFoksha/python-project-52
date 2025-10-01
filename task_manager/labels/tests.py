import unittest
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.messages import get_messages


class LabelTests(TestCase):
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
        self.task.labels.add(self.label)
        self.label_list_url = reverse('label_list')
        self.label_create_url = reverse('label_create')
        self.label_update_url = reverse(
            'label_update',
            kwargs={'pk': self.label.pk}
        )
        self.label_delete_url = reverse(
            'label_delete',
            kwargs={'pk': self.label.pk}
        )
        self.index_url = reverse('index')

    def test_label_list_view(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.get(self.label_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertContains(response, 'Тестовая метка')

    def test_label_list_unauthorized(self):
        response = self.client.get(self.label_list_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_label_create_success(self):
        self.client.login(username='testuser', password='TestPass123')
        form_data = {'name': 'Новая метка'}
        response = self.client.post(self.label_create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.label_list_url)
        self.assertTrue(Label.objects.filter(name='Новая метка').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно создана', str(messages[0]))

    def test_label_create_unauthorized(self):
        form_data = {'name': 'Новая метка'}
        response = self.client.post(self.label_create_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_label_update_success(self):
        self.client.login(username='testuser', password='TestPass123')
        form_data = {'name': 'Обновленная метка'}
        response = self.client.post(self.label_update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.label_list_url)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Обновленная метка')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Метка успешно изменена', str(messages[0]))

    def test_label_update_unauthorized(self):
        form_data = {'name': 'Обновленная метка'}
        response = self.client.post(self.label_update_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))

    def test_label_delete_success(self):
        self.client.login(username='testuser', password='TestPass123')
        label = Label.objects.create(name='Удаляемая метка')
        delete_url = reverse('label_delete', kwargs={'pk': label.pk})
        response = self.client.post(delete_url, {'confirm': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.label_list_url)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('успешно удалена', str(messages[0]))

    def test_label_delete_with_task(self):
        self.client.login(username='testuser', password='TestPass123')
        response = self.client.post(self.label_delete_url, {'confirm': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.label_list_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(
            'Невозможно удалить метку, связанную с задачами.',
            str(messages[0])
        )
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_unauthorized(self):
        response = self.client.post(self.label_delete_url, {'confirm': True})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Необходима авторизация пользователя', str(messages[0]))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())


if __name__ == '__main__':
    unittest.main()