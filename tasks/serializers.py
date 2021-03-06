from rest_framework import serializers, status
from rest_framework.response import Response

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = []

    def create(self, validated_data):
        request = self.context['request']
        task_users = validated_data.pop('task_user')
        if request.user not in task_users:
            task_users.append(request.user)
        task = Task.objects.create(**validated_data)
        task.created_by = request.user
        task.task_user.add(*task_users)
        task.save()
        return task


class MultipleTaskSerializer(serializers.Serializer):
    tasks = serializers.ListField()

    class Meta:
        fields = ['tasks']

    def create(self, validated_data):
        request = self.context['request']
        for i in validated_data['tasks']:
            Task.objects.create(body=i['body'], status=i['status'], created_by=request.user)
        return validated_data

