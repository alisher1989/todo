from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from tasks.models import Task


class IsTaskOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PUT']:
            return True
        # elif request.method in ['PUT', 'DELETE']:
        #     instance = Task.objects.get(pk=view.kwargs['pk'])
        #     return instance.created_by == request.user
        elif request.method == 'POST' and request.user.is_anonymous:
            return False
        return True