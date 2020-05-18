from django.contrib.auth.models import User
from django.db import models


def get_admin():
    return User.objects.get(username='admin').id


class Task(models.Model):
    TASK_STATUS = (
        ('active', 'active'),
        ('completed', 'completed'),
    )
    title = models.CharField(max_length=55, null=True, blank=True, verbose_name='название задачи')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='описание')
    status = models.CharField(max_length=55, choices=TASK_STATUS, null=True, blank=True, verbose_name='статус', default=TASK_STATUS[0][0])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    created_by = models.ForeignKey(User, max_length=40, null=True, blank=True, on_delete=models.CASCADE,
                            default=get_admin, verbose_name='Author', related_name='task_creator')
    task_user = models.ManyToManyField(User, blank=True, related_name='task_users', verbose_name='Пользователи задачи')

    def __str__(self):
        return self.title


