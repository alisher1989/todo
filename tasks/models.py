from django.contrib.auth.models import User
from django.db import models


def get_admin():
    return User.objects.get(username='admin').id


class Task(models.Model):
    TASK_STATUS = (
        ('active', 'active'),
        ('completed', 'completed'),
    )
    body = models.TextField(max_length=255, null=True, blank=True, verbose_name='Тело')
    status = models.CharField(max_length=55, choices=TASK_STATUS, null=True, blank=True, verbose_name='статус', default=TASK_STATUS[0][0])
    created_by = models.ForeignKey(User, max_length=40, null=True, blank=True, on_delete=models.CASCADE,
                            verbose_name='Author', related_name='task_creator')
    task_user = models.ManyToManyField(User, blank=True, related_name='task_users', verbose_name='Пользователи задачи')

    def __str__(self):
        return self.pk


