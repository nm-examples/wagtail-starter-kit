from django.contrib.auth.models import User
from django.test import TestCase

from app.home.models import HomePage


class HomeTestCase(TestCase):
    """Tests for the home app frontend and admin."""

    def setUp(self):
        """Create a test user for admin access."""
        # Create test user
        User.objects.create_user(
            username="testuser", password="12345", is_staff=True, is_superuser=True
        )

        # Get the existing home page
        self.home_page = HomePage.objects.first()

    def test_home_frontend_returns_200(self):
        """Test that the home page frontend returns 200 OK."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to your new Wagtail site!")
        self.assertTemplateUsed(response, "home/home_page.html")

    def test_home_admin_edit_returns_200(self):
        """Test that the home page admin edit page returns 200 OK."""
        self.client.login(username="testuser", password="12345")
        response = self.client.get(f"/admin/pages/{self.home_page.pk}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_home_admin_delete_returns_200(self):
        """Test that the home page admin delete page returns 200 OK."""
        self.client.login(username="testuser", password="12345")
        response = self.client.get(f"/admin/pages/{self.home_page.pk}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_home_admin_copy_returns_200(self):
        """Test that the home page admin copy page returns 200 OK."""
        self.client.login(username="testuser", password="12345")
        response = self.client.get(f"/admin/pages/{self.home_page.pk}/copy/")
        self.assertEqual(response.status_code, 200)

    def test_home_admin_move_returns_200(self):
        """Test that the home page admin move page returns 200 OK."""
        self.client.login(username="testuser", password="12345")
        response = self.client.get(f"/admin/pages/{self.home_page.pk}/move/")
        self.assertEqual(response.status_code, 200)

    def test_home_admin_history_returns_200(self):
        """Test that the home page admin history page returns 200 OK."""
        self.client.login(username="testuser", password="12345")
        response = self.client.get(f"/admin/pages/{self.home_page.pk}/history/")
        self.assertEqual(response.status_code, 200)
