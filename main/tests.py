from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import UserProfile


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")  # assuming you have named your urls
        self.register_url = reverse("register")
        self.upload_csv_url = reverse("upload_csv_to_analyze")
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.openai_api_key = settings.OPENAI_API_KEY

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_register_POST(self):
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser2",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEquals(
            response.status_code, 200
        )  # assuming successful registration redirects to home

    def test_upload_csv_GET(self):
        self.client.login(
            username="testuser", password="12345"
        )  # you need to be logged in
        response = self.client.get(self.upload_csv_url)
        self.assertEquals(response.status_code, 200)

    def test_upload_csv_POST(self):
        self.client.login(
            username="testuser", password="12345"
        )  # you need to be logged in
        file = SimpleUploadedFile(
            name="test.csv",
            content=b"Column1,Column2\nValue1,Value2\n",
            content_type="text/csv",
        )
        response = self.client.post(self.upload_csv_url, {"file": file.read()})
        self.assertEquals(response.status_code, 200)
