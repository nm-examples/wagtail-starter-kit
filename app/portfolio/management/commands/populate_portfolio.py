import random

from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from app.blog.models import BlogPage
from app.home.models import HomePage
from app.portfolio.models import PortfolioPage


class Command(BaseCommand):
    help = "Creates a portfolio page with sample content using the PortfolioStreamBlock"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing portfolio page if it exists",
        )
        parser.add_argument(
            "--title",
            type=str,
            default="Portfolio",
            help="Title for the portfolio page (default: 'Portfolio')",
        )

    def handle(self, *args, **options):
        try:
            # Get the home page
            home_page = HomePage.objects.first()
            if not home_page:
                self.stdout.write(
                    self.style.ERROR(
                        "No home page found. Please create a home page first."
                    )
                )
                return

            # Check if portfolio page already exists
            portfolio_page = home_page.get_children().type(PortfolioPage).first()

            if portfolio_page and not options["overwrite"]:
                self.stdout.write(
                    self.style.WARNING(
                        f"Portfolio page '{portfolio_page.title}' already exists. Use --overwrite to replace it."
                    )
                )
                return

            # Delete existing portfolio page if overwriting
            if portfolio_page and options["overwrite"]:
                portfolio_page.delete()
                self.stdout.write("Deleted existing portfolio page")

            # Create the new portfolio page
            new_portfolio_page = PortfolioPage(
                title=options["title"],
                slug="portfolio",
                show_in_menus=True,
                body=self.create_portfolio_content(),
            )

            # Add as child of home page
            home_page.add_child(instance=new_portfolio_page)
            new_portfolio_page.save_revision().publish()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created portfolio page: '{new_portfolio_page.title}'"
                )
            )
            self.stdout.write(f"  URL: /{new_portfolio_page.slug}/")
            self.stdout.write("  Show in menus: ✓")
            self.stdout.write(
                f"  Content blocks: {len(new_portfolio_page.body)} blocks"
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

    def create_portfolio_content(self):
        """Create sample portfolio content using the available stream blocks"""
        content_blocks = []

        # Add heading block
        content_blocks.append(
            ("heading_block", {"heading_text": "My Portfolio", "size": "h2"})
        )

        # Add paragraph block
        content_blocks.append(
            (
                "paragraph_block",
                "<p>Welcome to my portfolio! Here you'll find a showcase of my work, skills, and projects. "
                "I'm passionate about creating innovative solutions and bringing ideas to life through technology.</p>",
            )
        )

        # Add image block if images are available
        available_images = Image.objects.all()
        if available_images.exists():
            selected_image = random.choice(available_images)
            content_blocks.append(
                (
                    "image_block",
                    {
                        "image": selected_image,
                        "caption": "A showcase of creative work",
                        "attribution": "Portfolio showcase",
                    },
                )
            )
            self.stdout.write(f"Added portfolio image: {selected_image.title}")

        # Add skills section with card blocks
        content_blocks.extend(self.create_skills_section())

        # Add projects section with more card blocks
        content_blocks.extend(self.create_projects_section())

        # Add featured blog posts if blog pages exist
        featured_posts_block = self.create_featured_posts_block()
        if featured_posts_block:
            content_blocks.append(featured_posts_block)

        # Add contact section
        content_blocks.extend(self.create_contact_section())

        return content_blocks

    def create_skills_section(self):
        """Create skills section with card blocks"""
        blocks = []

        # Skills heading
        blocks.append(
            ("heading_block", {"heading_text": "Skills & Expertise", "size": "h2"})
        )

        # Skills description
        blocks.append(
            (
                "paragraph_block",
                "<p>Here are some of the key technologies and skills I work with:</p>",
            )
        )

        # Skills cards
        skills = [
            {
                "heading": "Web Development",
                "text": (
                    "<p>Building modern, responsive websites using "
                    "<strong>HTML5</strong>, <strong>CSS3</strong>, and "
                    "<strong>JavaScript</strong>. Experience with frameworks "
                    "like React, Vue.js, and Django.</p>"
                ),
            },
            {
                "heading": "Python & Django",
                "text": (
                    "<p>Developing robust web applications with "
                    "<strong>Python</strong> and <strong>Django</strong>. "
                    "Expertise in building APIs, handling databases, and "
                    "creating scalable solutions.</p>"
                ),
            },
            {
                "heading": "Content Management",
                "text": (
                    "<p>Creating powerful content management solutions with "
                    "<strong>Wagtail CMS</strong>. Building custom page types, "
                    "StreamFields, and admin interfaces.</p>"
                ),
            },
        ]

        available_images = Image.objects.all()
        for skill in skills:
            # Add random image to some cards
            image = None
            if available_images.exists() and random.choice([True, False]):
                image = random.choice(available_images)

            blocks.append(
                (
                    "card",
                    {
                        "heading": skill["heading"],
                        "text": skill["text"],
                        "image": image,
                    },
                )
            )

        return blocks

    def create_projects_section(self):
        """Create projects section with card blocks"""
        blocks = []

        # Projects heading
        blocks.append(
            ("heading_block", {"heading_text": "Recent Projects", "size": "h2"})
        )

        # Projects description
        blocks.append(
            (
                "paragraph_block",
                "<p>Take a look at some of my recent work and projects:</p>",
            )
        )

        # Project cards
        projects = [
            {
                "heading": "E-commerce Platform",
                "text": (
                    "<p>A full-featured online store built with "
                    "<strong>Django</strong> and <strong>Wagtail</strong>. "
                    "Features include product catalog, shopping cart, "
                    "payment processing, and order management.</p>"
                ),
            },
            {
                "heading": "Corporate Website",
                "text": (
                    "<p>A modern, responsive corporate website with custom "
                    "<strong>Wagtail</strong> page types, advanced content "
                    "management, and SEO optimization.</p>"
                ),
            },
            {
                "heading": "Blog Platform",
                "text": (
                    "<p>A content-rich blog platform with author management, "
                    "tagging system, comment functionality, and social media "
                    "integration built with <strong>Wagtail CMS</strong>.</p>"
                ),
            },
        ]

        available_images = Image.objects.all()
        for project in projects:
            # Add random image to projects
            image = None
            if available_images.exists():
                image = random.choice(available_images)

            blocks.append(
                (
                    "card",
                    {
                        "heading": project["heading"],
                        "text": project["text"],
                        "image": image,
                    },
                )
            )

        return blocks

    def create_featured_posts_block(self):
        """Create featured blog posts block if blog pages exist"""
        blog_pages = BlogPage.objects.live().order_by("-first_published_at")[:3]

        if blog_pages.exists():
            self.stdout.write(f"Added featured posts: {blog_pages.count()} blog posts")
            return (
                "featured_posts",
                {
                    "heading": "Featured Blog Posts",
                    "text": (
                        "<p>Check out some of my latest blog posts about web "
                        "development, technology, and best practices:</p>"
                    ),
                    "posts": list(blog_pages),
                },
            )

        self.stdout.write("No blog pages found - skipping featured posts block")
        return None

    def create_contact_section(self):
        """Create contact section"""
        blocks = []

        # Contact heading
        blocks.append(("heading_block", {"heading_text": "Get In Touch", "size": "h2"}))

        # Contact description
        blocks.append(
            (
                "paragraph_block",
                (
                    "<p>Interested in working together? I'd love to hear about "
                    "your project and discuss how I can help bring your ideas "
                    "to life.</p>"
                    "<p>Feel free to reach out through any of the following "
                    "channels:</p>"
                    "<ul>"
                    "<li><strong>Email:</strong> your.email@example.com</li>"
                    "<li><strong>LinkedIn:</strong> Connect with me on LinkedIn</li>"
                    "<li><strong>GitHub:</strong> Check out my code repositories</li>"
                    "</ul>"
                ),
            )
        )

        # Contact card
        blocks.append(
            (
                "card",
                {
                    "heading": "Let's Collaborate",
                    "text": (
                        "<p>Whether you need a new website, want to improve your "
                        "existing platform, or have an exciting project idea, "
                        "I'm here to help. Let's discuss your requirements and "
                        "create something amazing together!</p>"
                    ),
                    "image": None,
                },
            )
        )

        return blocks
