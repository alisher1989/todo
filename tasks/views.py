from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tasks.permissions import IsTaskOwner
from tasks.serializers import TaskSerializer, MultipleTaskSerializer


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


class MultipleTaskCreateView(ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = MultipleTaskSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = Task.objects.filter(created_by=self.request.user)
        return queryset
