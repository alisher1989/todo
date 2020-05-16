from django.urls import path
from tasks.views import TaskView

urlpatterns = [
    path('task/', TaskView.as_view({'get': 'list', 'post': 'create'})),
    path('task/<int:pk>/', TaskView.as_view({'get': 'retrieve', 'put': 'update'})),
]