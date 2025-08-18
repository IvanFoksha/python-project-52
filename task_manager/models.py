from django.db import models

class Status:
    name = models.CharField(max_length=100, unique=True, help_text='Название статуса')

    def __str__(self):
        return self.name

    def has_related_tasks(self):
        return False
