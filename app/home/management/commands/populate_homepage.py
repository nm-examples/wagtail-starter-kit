import random

from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from app.home.models import HomePage


class Command(BaseCommand):
    help = "Populates the existing home page with sample hero section and body content"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing content if it exists",
        )
        parser.add_argument(
            "--hero-text",
            type=str,
            default="Welcome to Your Amazing Wagtail Site",
            help="Hero text to display (default: 'Welcome to Your Amazing Wagtail Site')",
        )
        parser.add_argument(
            "--hero-cta",
            type=str,
            default="Explore Our Content",
            help="Hero call-to-action button text (default: 'Explore Our Content')",
        )

    def handle(self, *args, **options):
        try:
            # Get the existing home page
            home_page = HomePage.objects.get()

            # Check if content already exists
            has_hero_content = any(
                [
                    home_page.image,
                    home_page.hero_text,
                    home_page.hero_cta,
                    home_page.hero_cta_link,
                ]
            )
            has_body_content = bool(home_page.body)

            if (has_hero_content or has_body_content) and not options["overwrite"]:
                self.stdout.write(
                    self.style.WARNING(
                        "Home page already has content. Use --overwrite to replace it."
                    )
                )
                if has_hero_content:
                    self.stdout.write("  Hero section: ✓")
                if has_body_content:
                    self.stdout.write(
                        f"  Body content: {len(home_page.body)} characters"
                    )
                return

            # Populate hero section
            hero_image = self.populate_hero_section(home_page, options)

            # Populate body content
            image_embed = self.get_body_image_embed(hero_image)

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

            # Update the home page body content
            home_page.body = sample_content
            home_page.save()

            # Create a new revision to track the change
            home_page.save_revision().publish()

            success_message = "Successfully populated home page content:"
            self.stdout.write(self.style.SUCCESS(success_message))
            self.stdout.write("  Hero section: ✓")
            self.stdout.write(f"  Body content: {len(sample_content)} characters")
            if hero_image:
                self.stdout.write(f"  Images used: {hero_image.title}")

        except HomePage.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("No home page found. Please create a home page first.")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

    def populate_hero_section(self, home_page, options):
        """Populate the hero section fields and return the selected image"""
        # Get available images
        available_images = Image.objects.all()
        selected_image = None

        if available_images.exists():
            selected_image = random.choice(available_images)
            home_page.image = selected_image
            self.stdout.write(f"Selected hero image: {selected_image.title}")
        else:
            self.stdout.write("No images found - hero will be created without image")

        # Set hero text
        home_page.hero_text = options["hero_text"]

        # Set hero CTA
        home_page.hero_cta = options["hero_cta"]

        # Try to find a suitable page for CTA link
        cta_link = self.get_cta_link_page(home_page)
        if cta_link:
            home_page.hero_cta_link = cta_link
            self.stdout.write(f"Set CTA link to: {cta_link.title}")
        else:
            self.stdout.write("No suitable CTA link page found")

        return selected_image

    def get_cta_link_page(self, home_page):
        """Find a suitable page for the CTA link"""
        # Try to find blog index page first
        from app.blog.models import BlogIndexPage

        blog_index = BlogIndexPage.objects.live().first()
        if blog_index:
            return blog_index

        # Try to find portfolio page
        from app.portfolio.models import PortfolioPage

        portfolio_page = PortfolioPage.objects.live().first()
        if portfolio_page:
            return portfolio_page

        # Fall back to any child page of home
        child_pages = home_page.get_children().live()
        if child_pages.exists():
            return child_pages.first()

        return None

    def get_body_image_embed(self, hero_image):
        """Generate image embed code for body content (different from hero image if possible)"""
        available_images = Image.objects.all()

        if not available_images.exists():
            return ""

        # Try to use a different image than the hero image
        body_images = (
            available_images.exclude(id=hero_image.id)
            if hero_image
            else available_images
        )

        if body_images.exists():
            selected_image = random.choice(body_images)
        else:
            # Use hero image if no other images available
            selected_image = hero_image

        if selected_image:
            return (
                f'<embed alt="{selected_image.title}" embedtype="image" '
                f'format="left" id="{selected_image.id}"/>'
            )

        return ""
