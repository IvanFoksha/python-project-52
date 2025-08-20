from django.db import models


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
        return False
