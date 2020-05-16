from django.urls import path
from tasks.views import TaskView, MultipleTaskCreateView

urlpatterns = [
    path('task/', TaskView.as_view({'get': 'list', 'post': 'create'})),
    path('multi_task/', MultipleTaskCreateView.as_view({'get': 'list', 'post': 'create'})),
    path('task/<int:pk>/', TaskView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]