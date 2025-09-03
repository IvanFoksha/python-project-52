from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name=_('First Name')
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name=_('Last Name')
    )
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
