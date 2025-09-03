from django.db import models


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
