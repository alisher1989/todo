import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from accounts.models import Profile
from tasks.models import Task
from tasks.views import TaskView


class TasksViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="davinci", password="qwerty")
        self.profile = Profile.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.task = Task.objects.create(body='t', created_by=self.user)
        self.factory = APIRequestFactory()
        self.view = TaskView.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update'})

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_task_success(self):
        self.api_authentication()
        expected_body = 'tttt'
        data = {"body": expected_body, "description": "first desc", "status": "active", "created_by": "1", "task_user": [1]}
        url = reverse('task_list')
        response = self.client.post(url, data=data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.last().body, expected_body)
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_unsuccess(self):
        expected_title = 'first'
        data = {"body": expected_title, "status": "active", "created_by": "1", "task_user": [1]}
        url = reverse('task_list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_detail_retrieve(self):
        self.api_authentication()
        expected_body = 't'
        url = reverse('task_detail', kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.last().body, expected_body)

    def test_task_detail_update(self):
        self.api_authentication()
        expected_body = 'ttttitle'
        data = {'body': 'ttttitle'}
        url = reverse('task_detail', kwargs={"pk": self.task.pk})
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(Task.objects.last().body, expected_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_delete(self):
        self.api_authentication()
        url = reverse('task_detail', kwargs={"pk": self.task.pk})
        response = self.client.delete(url)
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_multiple_task_success(self):
        self.api_authentication()
        data = {
            "tasks": [{"body": "1", "status": "active", "task_user": []},
                      {"body": "2", "status": "closed", "task_user": []},
                      {"body": "3", "status": "active", "task_user": []}]
                }
        url = reverse('multi_task')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
