from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    class Meta:
        model = Task
        exclude = []

    # def get_user(self, obj):
    #     return obj.created_by.username

    def create(self, validated_data):
        request = self.context['request']
        task = Task.objects.create(**validated_data)
        task.created_by = request.user
        task.save()
        return validated_data