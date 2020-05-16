from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = []

    def create(self, validated_data):
        request = self.context['request']
        task = Task.objects.create(**validated_data)
        task.created_by = request.user
        task.save()
        return task


class MultipleTaskSerializer(serializers.Serializer):
    tasks = serializers.ListField()

    class Meta:
        fields = ['tasks']

    def create(self, validated_data):
        request = self.context['request']
        for i in validated_data['tasks']:
            Task.objects.create(title=i['title'], description=i['description'], status=i['status'], created_by=request.user)
        return validated_data

