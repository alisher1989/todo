from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.permissions import IsTaskOwner
from tasks.serializers import TaskSerializer


class TaskView(ModelViewSet):
    permission_classes = [IsTaskOwner]
    serializer_class = TaskSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = Task.objects.filter(created_by=self.request.user)
        return queryset
