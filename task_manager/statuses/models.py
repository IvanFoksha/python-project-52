from django.db import models
from django.contrib.auth.models import User
from task_manager.tasks.models import Task


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

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
