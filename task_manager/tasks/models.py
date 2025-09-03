from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


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
