from django.urls import path
from tasks.views import TaskView, MultipleTaskCreateView

urlpatterns = [
    path('task/', TaskView.as_view({'get': 'list', 'post': 'create'}), name='task_list'),
    path('multi_task/', MultipleTaskCreateView.as_view({'get': 'list', 'post': 'create'}), name='multi_task'),
    path('task/<int:pk>/', TaskView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task_detail'),
]