from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
import json

# Create your tests here.


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create_user(
            email="test@gmail.com", password="testpassword", username="test@gmail.com"
        )

    def test_register_user(self):
        url = reverse("signup")
        data = {
            "email": "test2@gmail.com",
            "password": "testpassword",
        }

        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["email"], data["email"])
        self.assertTrue(response.json()["token"])

    def test_login_user(self):
        url = reverse("login")
        data = {
            "email": "test@gmail.com",
            "password": "testpassword",
        }

        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], data["email"])
        self.assertTrue(response.json()["token"])
