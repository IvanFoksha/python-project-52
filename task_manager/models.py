from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Название статуса'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def has_related_tasks(self):
        return Task.objects.filter(status=self).exists()


class Task(models.Model):
    name = models.CharField(max_length=200, help_text='Название задачи')
    description = models.TextField(blank=True, help_text='Описание задачи')
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        help_text='Статус задачи'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_tasks',
        help_text='Автор задачи'
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        help_text='Исполнитель задачи'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        'Label',
        blank=True,
        help_text='Метки задачи'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Label(models.Model):
    name = models.CharField(max_length=100, help_text='Название метки')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def has_related_tasks(self):
        return self.task_set.exists()

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
