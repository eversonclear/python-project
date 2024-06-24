from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from appname.models.tasks import Task
import json

import jwt
from django.conf import settings


class TaskViewsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@gmail.com",
        )

        Task.objects.create(
            title="Task Title", description="Task Description", user_id=user.id
        )

        Task.objects.create(
            title="Task Title 2", description="Task Description 2", user_id=user.id
        )

        self.client = Client()
        self.valid_token = jwt.encode(
            {"user_id": user.id},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    def test_get_tasks(self):
        url = reverse("task_views")

        response = self.client.get(
            url,
            headers={"AUTHORIZATION": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["title"], "Task Title")
        self.assertEqual(response.json()[1]["title"], "Task Title 2")

    def test_get_tasks_unauthorized(self):
        url = reverse("task_views")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_create_task(self):
        url = reverse("task_views")

        response = self.client.post(
            url,
            data=json.dumps(
                {"title": "Task Title 3", "description": "Task Description 3"}
            ),
            content_type="application/json",
            headers={"AUTHORIZATION": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.last().title, "Task Title 3")
        self.assertEqual(Task.objects.last().description, "Task Description 3")
        self.assertEqual(Task.objects.last().user_id, 1)
        self.assertEqual(Task.objects.last().complete, False)

    def test_create_task_unauthorized(self):
        url = reverse("task_views")
        response = self.client.post(
            url,
            data=json.dumps(
                {"title": "Task Title 3", "description": "Task Description 3"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_update_task(self):
        task = Task.objects.first()
        url = reverse("task_detail_views", args=[task.id])

        response = self.client.put(
            url,
            data=json.dumps({"title": "Updated Task Title"}),
            content_type="application/json",
            headers={"AUTHORIZATION": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.first().title, "Updated Task Title")

    def test_update_task_unauthorized(self):
        task = Task.objects.first()
        url = reverse("task_detail_views", args=[task.id])

        response = self.client.put(
            url,
            data=json.dumps({"title": "Updated Task Title"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_delete_task(self):
        task = Task.objects.first()
        url = reverse("task_detail_views", args=[task.id])

        response = self.client.delete(
            url,
            headers={"AUTHORIZATION": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 1)

    def test_delete_task_unauthorized(self):
        task = Task.objects.first()
        url = reverse("task_detail_views", args=[task.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_get_task(self):
        task = Task.objects.first()
        url = reverse("task_detail_views", args=[task.id])

        response = self.client.get(
            url,
            headers={"AUTHORIZATION": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Task Title")

    def test_get_task_not_found(self):
        url = reverse("task_detail_views", args=[5])

        response = self.client.get(
            url,
            headers={"AUTHORIZATION": f"Bearer {self.valid_token}"},
        )

        self.assertEqual(response.status_code, 404)

    def test_get_task_unauthorized(self):
        task = Task.objects.first()
        url = reverse("task_detail_views", args=[task.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
