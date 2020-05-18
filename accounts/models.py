from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    description = models.CharField(null=True, blank=True, max_length=155)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

