from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file

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

    def test_populate_homepage_command(self):
        """Test the populate_homepage management command"""
        home_page = HomePage.objects.first()

        # Ensure home page starts with empty body
        home_page.body = ""
        home_page.save()

        # Create output capture
        out = StringIO()

        # Run the command
        call_command("populate_homepage", stdout=out)

        # Refresh from database
        home_page.refresh_from_db()

        # Check that body content was added
        self.assertNotEqual(home_page.body, "")
        self.assertIn("Welcome to Your Wagtail Site", home_page.body)
        self.assertIn("Successfully populated home page body content", out.getvalue())

    def test_populate_homepage_command_with_existing_content(self):
        """Test the populate_homepage management command when content already exists"""
        home_page = HomePage.objects.first()

        # Set some existing content
        home_page.body = "Existing content"
        home_page.save()

        # Create output capture
        out = StringIO()

        # Run the command without overwrite
        call_command("populate_homepage", stdout=out)

        # Refresh from database
        home_page.refresh_from_db()

        # Check that content wasn't changed
        self.assertEqual(home_page.body, "Existing content")
        self.assertIn("already has body content", out.getvalue())

    def test_populate_homepage_command_with_overwrite(self):
        """Test the populate_homepage management command with overwrite option"""
        home_page = HomePage.objects.first()

        # Set some existing content
        home_page.body = "Existing content"
        home_page.save()

        # Create output capture
        out = StringIO()

        # Run the command with overwrite
        call_command("populate_homepage", "--overwrite", stdout=out)

        # Refresh from database
        home_page.refresh_from_db()

        # Check that content was changed
        self.assertNotEqual(home_page.body, "Existing content")
        self.assertIn("Welcome to Your Wagtail Site", home_page.body)
        self.assertIn("Successfully populated home page body content", out.getvalue())

    def test_populate_homepage_command_with_image(self):
        """Test the populate_homepage command when images are available"""
        home_page = HomePage.objects.first()

        # Create a test image
        Image.objects.create(
            title="Test Image",
            file=get_test_image_file(),
        )

        # Ensure home page starts with empty body
        home_page.body = ""
        home_page.save()

        # Create output capture
        out = StringIO()

        # Run the command
        call_command("populate_homepage", stdout=out)

        # Refresh from database
        home_page.refresh_from_db()

        # Check that body content was added with image
        self.assertNotEqual(home_page.body, "")
        self.assertIn("Welcome to Your Wagtail Site", home_page.body)
        self.assertIn('embedtype="image"', home_page.body)
        self.assertIn("Selected image:", out.getvalue())
        self.assertIn("with image:", out.getvalue())

    def test_populate_homepage_command_without_images(self):
        """Test the populate_homepage command when no images are available"""
        home_page = HomePage.objects.first()

        # Remove all images
        Image.objects.all().delete()

        # Ensure home page starts with empty body
        home_page.body = ""
        home_page.save()

        # Create output capture
        out = StringIO()

        # Run the command
        call_command("populate_homepage", stdout=out)

        # Refresh from database
        home_page.refresh_from_db()

        # Check that body content was added without image
        self.assertNotEqual(home_page.body, "")
        self.assertIn("Welcome to Your Wagtail Site", home_page.body)
        self.assertNotIn('embedtype="image"', home_page.body)
        self.assertIn("No images found", out.getvalue())
