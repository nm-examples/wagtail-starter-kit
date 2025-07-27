from django.core.management.base import BaseCommand

from app.base.models import FooterText, NavigationSettings


class Command(BaseCommand):
    help = "Populates the NavigationSettings with sample social media URLs and FooterText with sample content"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing navigation settings if they exist",
        )
        parser.add_argument(
            "--linkedin",
            type=str,
            default="https://www.linkedin.com/company/torchbox",
            help="LinkedIn URL to set (default: https://www.linkedin.com/company/torchbox)",
        )
        parser.add_argument(
            "--github",
            type=str,
            default="https://github.com/wagtail/wagtail",
            help="GitHub URL to set (default: https://github.com/wagtail/wagtail)",
        )
        parser.add_argument(
            "--mastodon",
            type=str,
            default="https://fosstodon.org/@wagtail",
            help="Mastodon URL to set (default: https://fosstodon.org/@wagtail)",
        )
        parser.add_argument(
            "--footer-text",
            type=str,
            default="<p>&copy; 2024 Your Company. Built with <a href='https://wagtail.org/'>Wagtail</a>.</p>",
            help="Footer text content (HTML allowed, default: copyright notice with Wagtail link)",
        )

    def handle(self, *args, **options):
        try:
            # Handle NavigationSettings
            self.populate_navigation_settings(options)

            # Handle FooterText
            self.populate_footer_text(options)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

    def populate_navigation_settings(self, options):
        """Create or update NavigationSettings with social media URLs"""
        try:
            # Get or create NavigationSettings (BaseGenericSetting doesn't have site field)
            navigation_settings, created = NavigationSettings.objects.get_or_create()

            # Check if settings already exist and if we should overwrite
            if not created and not options["overwrite"]:
                existing_urls = []
                if navigation_settings.linkedin_url:
                    existing_urls.append(
                        f"LinkedIn: {navigation_settings.linkedin_url}"
                    )
                if navigation_settings.github_url:
                    existing_urls.append(f"GitHub: {navigation_settings.github_url}")
                if navigation_settings.mastodon_url:
                    existing_urls.append(
                        f"Mastodon: {navigation_settings.mastodon_url}"
                    )

                if existing_urls:
                    self.stdout.write(
                        self.style.WARNING(
                            "NavigationSettings already exist with content. Use --overwrite to replace:"
                        )
                    )
                    for url in existing_urls:
                        self.stdout.write(f"  {url}")
                    return

            # Update the settings with provided URLs
            navigation_settings.linkedin_url = options["linkedin"]
            navigation_settings.github_url = options["github"]
            navigation_settings.mastodon_url = options["mastodon"]
            navigation_settings.save()

            # Create success message
            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action} NavigationSettings with social media URLs:"
                )
            )
            self.stdout.write(f"  LinkedIn: {navigation_settings.linkedin_url}")
            self.stdout.write(f"  GitHub: {navigation_settings.github_url}")
            self.stdout.write(f"  Mastodon: {navigation_settings.mastodon_url}")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error populating NavigationSettings: {str(e)}")
            )

    def populate_footer_text(self, options):
        """Create or update FooterText with sample content"""
        try:
            # Get existing FooterText or create new one
            footer_text = FooterText.objects.first()

            if footer_text and not options["overwrite"]:
                # Check if footer has meaningful content (not just empty tags)
                import re

                # Remove HTML tags and whitespace to check for actual content
                text_content = re.sub(r"<[^>]*>", "", footer_text.body).strip()
                if text_content:
                    self.stdout.write(
                        self.style.WARNING(
                            "FooterText already exists with content. Use --overwrite to replace:"
                        )
                    )
                    # Show truncated version of existing content
                    content_preview = (
                        footer_text.body[:100] + "..."
                        if len(footer_text.body) > 100
                        else footer_text.body
                    )
                    self.stdout.write(f"  Current content: {content_preview}")
                    return

            # Create new FooterText if none exists
            if not footer_text:
                footer_text = FooterText()
                created = True
            else:
                created = False

            # Set the footer content
            footer_text.body = options["footer_text"]
            footer_text.save()

            # Create revision and publish (FooterText uses RevisionMixin)
            footer_text.save_revision().publish()

            # Create success message
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} FooterText:"))
            # Show truncated version of content
            content_preview = (
                footer_text.body[:100] + "..."
                if len(footer_text.body) > 100
                else footer_text.body
            )
            self.stdout.write(f"  Content: {content_preview}")

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error populating FooterText: {str(e)}")
            )
