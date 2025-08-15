import random

from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from app.home.models import HomePage


class Command(BaseCommand):
    help = "Populates the existing home page with sample body content"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing body content if it exists",
        )

    def handle(self, *args, **options):
        try:
            # Get the existing home page
            home_page = HomePage.objects.get()

            # Check if body content already exists
            if home_page.body and not options["overwrite"]:
                self.stdout.write(
                    self.style.WARNING(
                        "Home page already has body content. Use --overwrite to replace it."
                    )
                )
                self.stdout.write(
                    f"Current content length: {len(home_page.body)} characters"
                )
                return

            # Check for existing images
            available_images = Image.objects.all()
            selected_image = None
            image_embed = ""
            hero_image = None
            hero_text = None
            hero_cta = None

            if available_images.exists():
                # Select a random image
                selected_image = random.choice(available_images)
                # Create embed code for the image
                image_embed = (
                    f'<embed alt="{selected_image.title}" embedtype="image" '
                    f'format="left" id="{selected_image.id}"/>'
                )
                self.stdout.write(f"Selected image: {selected_image.title}")
                # Set hero section fields if they are not already set
                hero_image = selected_image
                hero_text = "Your Hero Section Title"
                hero_cta = "Your Hero Section CTA, you need to set a link"
            else:
                self.stdout.write(
                    "No images found - content will be created without images"
                )

            # Sample body content with optional image
            sample_content = f"""
<h2>Welcome to Your Wagtail Site</h2>

<p>This is your homepage, built with <strong>Wagtail CMS</strong>. Wagtail is a powerful,
developer-friendly content management system built on Django that makes it easy to create
beautiful, engaging websites.</p>

{image_embed}

<h3>Getting Started</h3>

<p>You can edit this content by going to the <a href="/admin/">Wagtail admin</a> and
selecting your home page. From there, you can:</p>

<ul>
    <li>Add and edit content using the rich text editor</li>
    <li>Create new pages and organize your site structure</li>
    <li>Upload and manage images and documents</li>
    <li>Customize your site's design and functionality</li>
</ul>

<h3>Features</h3>

<p>This starter kit includes:</p>

<ul>
    <li><strong>Docker Development Environment</strong> - Easy setup and consistent development experience</li>
    <li><strong>Multiple Database Options</strong> - PostgreSQL, MySQL, or SQLite3</li>
    <li><strong>Frontend Build Tools</strong> - SASS compilation and JavaScript bundling</li>
    <li><strong>Pico CSS Framework</strong> - Clean, semantic styling</li>
    <li><strong>Management Commands</strong> - Useful utilities for development and testing</li>
</ul>

<h3>Next Steps</h3>

<p>Now that you have your site running, consider:</p>

<ol>
    <li>Exploring the <a href="/style-guide/">Style Guide</a> to see available components</li>
    <li>Reading the <a href="https://docs.wagtail.org/">Wagtail documentation</a> to learn more</li>
    <li>Creating custom page types for your specific needs</li>
    <li>Setting up your production deployment</li>
</ol>

<p><em>Happy building with Wagtail!</em></p>
            """.strip()

            if hero_image:
                # Update the hero section fields
                home_page.image = hero_image
                home_page.hero_text = hero_text
                home_page.hero_cta = hero_cta

            # Update the home page body content
            home_page.body = sample_content
            home_page.save()

            # Create a new revision to track the change
            home_page.save_revision().publish()

            success_message = f"Successfully populated home page body content ({len(sample_content)} characters)"
            if selected_image:
                success_message += f" with image: {selected_image.title}"

            self.stdout.write(self.style.SUCCESS(success_message))

        except HomePage.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("No home page found. Please create a home page first.")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
