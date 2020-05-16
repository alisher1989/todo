from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from tasks.models import Task


class IsTaskOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or 'POST':
            return True
        else:
            instance = Task.objects.get(pk=view.kwargs['pk'])
            return request.user == instance.created_by