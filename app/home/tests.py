from django.contrib.auth.models import User
from django.test import TestCase

from app.home.models import HomePage


class HomeTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser", password="12345", is_staff=True, is_superuser=True
        ).save()

    def test_home_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wagtail Blog Tutorial")
        self.assertTemplateUsed(response, "home/home_page.html")

    def test_home_admin(self):
        self.client.login(username="testuser", password="12345")
        home_page = HomePage.objects.first()
        response = self.client.get(f"/admin/pages/{home_page.pk}/")
        self.assertEqual(response.status_code, 200)
