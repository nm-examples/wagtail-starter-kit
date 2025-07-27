from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Site

from app.base.models import FooterText, NavigationSettings


class PopulateSettingsTestCase(TestCase):
    def setUp(self):
        # Ensure there's a default site for testing
        if not Site.objects.filter(is_default_site=True).exists():
            Site.objects.create(
                hostname="localhost",
                port=8000,
                is_default_site=True,
            )

    def test_populate_settings_basic(self):
        """Test basic populate_settings command execution"""
        out = StringIO()

        # Run the command with default values
        call_command("populate_settings", stdout=out)

        # Check that NavigationSettings was created
        navigation_settings = NavigationSettings.objects.first()
        self.assertIsNotNone(navigation_settings)
        self.assertEqual(
            navigation_settings.linkedin_url,
            "https://www.linkedin.com/company/torchbox",
        )
        self.assertEqual(
            navigation_settings.github_url, "https://github.com/wagtail/wagtail"
        )
        self.assertEqual(
            navigation_settings.mastodon_url, "https://fosstodon.org/@wagtail"
        )

        # Check that FooterText was created
        footer_text = FooterText.objects.first()
        self.assertIsNotNone(footer_text)
        self.assertIn("&copy; 2024 Your Company", footer_text.body)
        self.assertIn("wagtail.org", footer_text.body)

        # Check success messages
        output = out.getvalue()
        self.assertIn("Created NavigationSettings with social media URLs", output)
        self.assertIn("Created FooterText", output)

    def test_populate_settings_with_custom_values(self):
        """Test populate_settings command with custom values"""
        out = StringIO()

        # Run the command with custom values
        call_command(
            "populate_settings",
            "--linkedin",
            "https://linkedin.com/company/testcompany",
            "--github",
            "https://github.com/testorg",
            "--mastodon",
            "https://mastodon.social/@testuser",
            "--footer-text",
            "<p>&copy; 2024 Test Company. All rights reserved.</p>",
            stdout=out,
        )

        # Check NavigationSettings values
        navigation_settings = NavigationSettings.objects.first()
        self.assertEqual(
            navigation_settings.linkedin_url, "https://linkedin.com/company/testcompany"
        )
        self.assertEqual(navigation_settings.github_url, "https://github.com/testorg")
        self.assertEqual(
            navigation_settings.mastodon_url, "https://mastodon.social/@testuser"
        )

        # Check FooterText value
        footer_text = FooterText.objects.first()
        self.assertEqual(
            footer_text.body, "<p>&copy; 2024 Test Company. All rights reserved.</p>"
        )

        # Check output contains custom values
        output = out.getvalue()
        self.assertIn("https://linkedin.com/company/testcompany", output)
        self.assertIn("https://github.com/testorg", output)
        self.assertIn("https://mastodon.social/@testuser", output)

    def test_populate_settings_with_existing_navigation_settings(self):
        """Test populate_settings when NavigationSettings already exist"""
        # Create existing NavigationSettings
        existing_nav = NavigationSettings.objects.create(
            linkedin_url="https://linkedin.com/existing",
            github_url="https://github.com/existing",
            mastodon_url="https://mastodon.social/@existing",
        )

        out = StringIO()

        # Run command without overwrite
        call_command("populate_settings", stdout=out)

        # Check that existing settings weren't changed
        existing_nav.refresh_from_db()
        self.assertEqual(existing_nav.linkedin_url, "https://linkedin.com/existing")
        self.assertEqual(existing_nav.github_url, "https://github.com/existing")
        self.assertEqual(existing_nav.mastodon_url, "https://mastodon.social/@existing")

        # Check warning message
        output = out.getvalue()
        self.assertIn("NavigationSettings already exist with content", output)
        self.assertIn("Use --overwrite to replace", output)

    def test_populate_settings_with_existing_footer_text(self):
        """Test populate_settings when FooterText already exists"""
        # Create existing FooterText
        existing_footer = FooterText.objects.create(
            body="<p>Existing footer content</p>"
        )
        existing_footer.save_revision().publish()

        out = StringIO()

        # Run command without overwrite
        call_command("populate_settings", stdout=out)

        # Check that existing footer wasn't changed
        existing_footer.refresh_from_db()
        self.assertEqual(existing_footer.body, "<p>Existing footer content</p>")

        # Check warning message
        output = out.getvalue()
        self.assertIn("FooterText already exists with content", output)
        self.assertIn("Use --overwrite to replace", output)

    def test_populate_settings_overwrite_navigation_settings(self):
        """Test populate_settings with --overwrite for NavigationSettings"""
        # Create existing NavigationSettings
        NavigationSettings.objects.create(
            linkedin_url="https://linkedin.com/old",
            github_url="https://github.com/old",
            mastodon_url="https://mastodon.social/@old",
        )

        out = StringIO()

        # Run command with overwrite
        call_command(
            "populate_settings",
            "--overwrite",
            "--linkedin",
            "https://linkedin.com/new",
            "--github",
            "https://github.com/new",
            "--mastodon",
            "https://mastodon.social/@new",
            stdout=out,
        )

        # Check that settings were updated
        navigation_settings = NavigationSettings.objects.first()
        self.assertEqual(navigation_settings.linkedin_url, "https://linkedin.com/new")
        self.assertEqual(navigation_settings.github_url, "https://github.com/new")
        self.assertEqual(
            navigation_settings.mastodon_url, "https://mastodon.social/@new"
        )

        # Check success message
        output = out.getvalue()
        self.assertIn("Updated NavigationSettings with social media URLs", output)

    def test_populate_settings_overwrite_footer_text(self):
        """Test populate_settings with --overwrite for FooterText"""
        # Create existing FooterText
        existing_footer = FooterText.objects.create(body="<p>Old footer content</p>")
        existing_footer.save_revision().publish()

        out = StringIO()

        # Run command with overwrite
        call_command(
            "populate_settings",
            "--overwrite",
            "--footer-text",
            "<p>New footer content</p>",
            stdout=out,
        )

        # Check that footer was updated
        footer_text = FooterText.objects.first()
        self.assertEqual(footer_text.body, "<p>New footer content</p>")

        # Check success message
        output = out.getvalue()
        self.assertIn("Updated FooterText", output)

    def test_populate_settings_empty_existing_navigation_settings(self):
        """Test populate_settings when NavigationSettings exist but are empty"""
        # Create NavigationSettings with empty fields
        NavigationSettings.objects.create(
            linkedin_url="", github_url="", mastodon_url=""
        )

        out = StringIO()

        # Run command without overwrite (should proceed since fields are empty)
        call_command("populate_settings", stdout=out)

        # Check that settings were populated
        navigation_settings = NavigationSettings.objects.first()
        self.assertEqual(
            navigation_settings.linkedin_url,
            "https://www.linkedin.com/company/torchbox",
        )
        self.assertEqual(
            navigation_settings.github_url, "https://github.com/wagtail/wagtail"
        )
        self.assertEqual(
            navigation_settings.mastodon_url, "https://fosstodon.org/@wagtail"
        )

        # Should show "Updated" since the object existed
        output = out.getvalue()
        self.assertIn("Updated NavigationSettings with social media URLs", output)

    def test_populate_settings_minimal_existing_footer_text(self):
        """Test populate_settings when FooterText exists with minimal content"""
        # Create FooterText with minimal body content (RichTextField can't be truly empty)
        existing_footer = FooterText.objects.create(body="<p></p>")
        existing_footer.save_revision().publish()

        out = StringIO()

        # Run command without overwrite (should proceed since body is minimal)
        call_command("populate_settings", stdout=out)

        # Check that footer was populated with new content
        footer_text = FooterText.objects.first()
        self.assertIn("&copy; 2024 Your Company", footer_text.body)

        # Should show "Updated" since the object existed
        output = out.getvalue()
        self.assertIn("Updated FooterText", output)

    def test_footer_text_revision_and_publish(self):
        """Test that FooterText is properly published with revisions"""
        out = StringIO()

        # Run the command
        call_command("populate_settings", stdout=out)

        # Check that FooterText was created and published
        footer_text = FooterText.objects.first()
        self.assertIsNotNone(footer_text)
        self.assertTrue(footer_text.live)
        self.assertIsNotNone(footer_text.latest_revision)

    def test_navigation_settings_model_type(self):
        """Test that NavigationSettings is properly created as BaseGenericSetting"""
        out = StringIO()

        # Run the command
        call_command("populate_settings", stdout=out)

        # Check that only one NavigationSettings instance exists (global setting)
        self.assertEqual(NavigationSettings.objects.count(), 1)

        navigation_settings = NavigationSettings.objects.first()
        self.assertIsNotNone(navigation_settings)

    def test_command_handles_multiple_runs(self):
        """Test that command can be run multiple times safely"""
        out1 = StringIO()
        out2 = StringIO()

        # Run command first time
        call_command("populate_settings", stdout=out1)

        # Run command second time without overwrite
        call_command("populate_settings", stdout=out2)

        # Should still only have one instance of each model
        self.assertEqual(NavigationSettings.objects.count(), 1)
        self.assertEqual(FooterText.objects.count(), 1)

        # Second run should show warnings about existing content
        output2 = out2.getvalue()
        self.assertIn("already exist", output2)
