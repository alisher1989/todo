import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_auth.tests.mixins import APIClient
from rest_auth.views import LoginView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
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
        expected_title = 'first'
        data = {"title": expected_title, "description": "first desc", "status": "active", "created_by": "1", "task_user": [1]}
        url = reverse('task_list')
        response = self.client.post(url, data=data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.last().title, expected_title)
        self.assertEqual(Task.objects.count(), 1)
        print(status.HTTP_201_CREATED)

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
        print(status.HTTP_200_OK)

    def test_task_detail_update(self):
        self.api_authentication()
        expected_body = 'ttttitle'
        data = {'body': 'ttttitle'}
        url = reverse('task_detail', kwargs={"pk": self.task.pk})
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(Task.objects.last().body, expected_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_create_multiple_task_success(self):
    #     self.api_authentication()
    #     # expected_title = 'first'
    #     data = {"title": expected_title, "description": "first desc", "status": "active", "created_by": "1", "task_user": [1]}
    #     url = reverse('multi_task')
    #     response = self.client.post(url, data=data, format='json')
    #     print(response.json())
    #     # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # self.assertEqual(Task.objects.last().title, expected_title)
    #     # self.assertEqual(Task.objects.count(), 1)
    #     print(status.HTTP_201_CREATED)
