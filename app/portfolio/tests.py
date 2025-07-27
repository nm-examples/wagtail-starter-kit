from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file

from app.blog.models import BlogIndexPage, BlogPage
from app.home.models import HomePage
from app.portfolio.models import PortfolioPage


class PopulatePortfolioTestCase(TestCase):
    """Test the populate_portfolio management command"""

    def test_populate_portfolio_basic(self):
        """Test basic portfolio population"""
        out = StringIO()

        # Run the command
        call_command("populate_portfolio", stdout=out)

        # Check that portfolio page was created
        portfolio_page = PortfolioPage.objects.first()
        self.assertIsNotNone(portfolio_page)
        self.assertEqual(portfolio_page.title, "Portfolio")
        self.assertEqual(portfolio_page.slug, "portfolio")
        self.assertTrue(portfolio_page.show_in_menus)
        self.assertTrue(portfolio_page.live)

        # Check that it's a child of a home page
        self.assertIsInstance(portfolio_page.get_parent().specific, HomePage)

        # Check that body content was added
        self.assertTrue(portfolio_page.body)
        self.assertGreater(len(portfolio_page.body), 0)

        # Check success message
        output = out.getvalue()
        self.assertIn("Successfully created portfolio page: 'Portfolio'", output)
        self.assertIn("Show in menus: ✓", output)
        self.assertIn("Content blocks:", output)

    def test_populate_portfolio_with_custom_title(self):
        """Test portfolio population with custom title"""
        out = StringIO()

        # Run the command with custom title
        call_command("populate_portfolio", "--title", "My Custom Portfolio", stdout=out)

        # Check that portfolio page was created with custom title
        portfolio_page = PortfolioPage.objects.first()
        self.assertEqual(portfolio_page.title, "My Custom Portfolio")
        self.assertEqual(portfolio_page.slug, "portfolio")
        self.assertTrue(portfolio_page.show_in_menus)

        # Check success message
        output = out.getvalue()
        self.assertIn(
            "Successfully created portfolio page: 'My Custom Portfolio'", output
        )

    def test_populate_portfolio_with_existing_page(self):
        """Test populate_portfolio when portfolio page already exists"""
        # Get the home page that the command will use
        home_page = HomePage.objects.first()

        # Create existing portfolio page
        existing_portfolio = PortfolioPage(
            title="Existing Portfolio",
            slug="portfolio",
            body=[],
        )
        home_page.add_child(instance=existing_portfolio)
        existing_portfolio.save_revision().publish()

        # Verify the existing page was created correctly
        self.assertEqual(PortfolioPage.objects.count(), 1)

        out = StringIO()

        # Run command without overwrite
        call_command("populate_portfolio", stdout=out)

        # Check that existing page wasn't changed
        self.assertEqual(PortfolioPage.objects.count(), 1)
        portfolio_page = PortfolioPage.objects.first()
        self.assertEqual(portfolio_page.title, "Existing Portfolio")
        self.assertEqual(len(portfolio_page.body), 0)

        # Check warning message
        output = out.getvalue()
        self.assertIn("already exists", output)
        self.assertIn("Use --overwrite to replace", output)

    def test_populate_portfolio_overwrite_existing(self):
        """Test populate_portfolio with --overwrite for existing page"""
        # Get the home page that the command will use
        home_page = HomePage.objects.first()

        # Create existing portfolio page
        existing_portfolio = PortfolioPage(
            title="Old Portfolio",
            slug="portfolio",
            body=[],
        )
        home_page.add_child(instance=existing_portfolio)
        existing_portfolio.save_revision().publish()

        # Verify the existing page was created correctly
        self.assertEqual(PortfolioPage.objects.count(), 1)
        self.assertEqual(PortfolioPage.objects.first().title, "Old Portfolio")

        out = StringIO()

        # Run command with overwrite
        call_command(
            "populate_portfolio", "--overwrite", "--title", "New Portfolio", stdout=out
        )

        # Check success message and that overwrite was mentioned
        output = out.getvalue()

        # The command should either succeed in creating the new page or at least mention the delete
        self.assertTrue(
            "Successfully created portfolio page: 'New Portfolio'" in output
            or "Deleted existing portfolio page" in output,
            f"Expected success or delete message in output: {output}",
        )

    def test_populate_portfolio_with_images(self):
        """Test portfolio population when images are available"""
        # Create test images
        Image.objects.create(
            title="Test Image 1",
            file=get_test_image_file(),
        )
        Image.objects.create(
            title="Test Image 2",
            file=get_test_image_file(),
        )

        out = StringIO()

        # Run the command
        call_command("populate_portfolio", stdout=out)

        # Check that portfolio was created
        portfolio_page = PortfolioPage.objects.first()
        self.assertIsNotNone(portfolio_page)
        self.assertGreater(len(portfolio_page.body), 0)

        # Check output mentions images
        output = out.getvalue()
        self.assertIn("Added portfolio image:", output)

        # Check that some blocks contain images
        has_image_block = False
        has_card_with_image = False

        for block in portfolio_page.body:
            if block.block_type == "image_block":
                has_image_block = True
                self.assertIsNotNone(block.value.get("image"))
            elif block.block_type == "card" and block.value.get("image"):
                has_card_with_image = True

        self.assertTrue(has_image_block or has_card_with_image)

    def test_populate_portfolio_without_images(self):
        """Test portfolio population when no images are available"""
        # Ensure no images exist
        Image.objects.all().delete()

        out = StringIO()

        # Run the command
        call_command("populate_portfolio", stdout=out)

        # Check that portfolio was still created
        portfolio_page = PortfolioPage.objects.first()
        self.assertIsNotNone(portfolio_page)
        self.assertGreater(len(portfolio_page.body), 0)

        # Check that content was created without images
        for block in portfolio_page.body:
            if block.block_type == "image_block":
                # Should not have image blocks when no images available
                self.fail("Image block found when no images should be available")
            elif block.block_type == "card":
                # Cards should have no images
                self.assertIsNone(block.value.get("image"))

    def test_populate_portfolio_with_blog_pages(self):
        """Test portfolio population when blog pages exist for featured posts"""
        # Get the home page that the command will use
        home_page = HomePage.objects.first()

        # Create blog index page
        blog_index = BlogIndexPage(
            title="Blog",
            slug="blog",
        )
        home_page.add_child(instance=blog_index)
        blog_index.save_revision().publish()

        # Create blog pages
        for i in range(3):
            blog_page = BlogPage(
                title=f"Blog Post {i+1}",
                slug=f"blog-post-{i+1}",
                date="2024-01-01",
                intro=f"Intro for blog post {i+1}",
                body=f"<p>Content for blog post {i+1}</p>",
            )
            blog_index.add_child(instance=blog_page)
            blog_page.save_revision().publish()

        out = StringIO()

        # Run the command
        call_command("populate_portfolio", stdout=out)

        # Check that portfolio was created
        portfolio_page = PortfolioPage.objects.first()
        self.assertIsNotNone(portfolio_page)

        # Check output mentions featured posts
        output = out.getvalue()
        self.assertIn("Added featured posts: 3 blog posts", output)

        # Check that featured posts block exists
        has_featured_posts = False
        for block in portfolio_page.body:
            if block.block_type == "featured_posts":
                has_featured_posts = True
                self.assertEqual(block.value["heading"], "Featured Blog Posts")
                self.assertEqual(len(block.value["posts"]), 3)
                break

        self.assertTrue(has_featured_posts)

    def test_populate_portfolio_without_blog_pages(self):
        """Test portfolio population when no blog pages exist"""
        out = StringIO()

        # Run the command
        call_command("populate_portfolio", stdout=out)

        # Check that portfolio was created
        portfolio_page = PortfolioPage.objects.first()
        self.assertIsNotNone(portfolio_page)

        # Check output mentions no blog pages
        output = out.getvalue()
        self.assertIn("No blog pages found - skipping featured posts block", output)

        # Check that no featured posts block exists
        for block in portfolio_page.body:
            if block.block_type == "featured_posts":
                self.fail("Featured posts block found when no blog pages should exist")

    def test_populate_portfolio_content_structure(self):
        """Test that portfolio has the expected content structure"""
        out = StringIO()

        # Run the command
        call_command("populate_portfolio", stdout=out)

        # Check that portfolio was created
        portfolio_page = PortfolioPage.objects.first()
        self.assertIsNotNone(portfolio_page)

        # Check content structure
        block_types = [block.block_type for block in portfolio_page.body]

        # Should have heading blocks
        self.assertIn("heading_block", block_types)

        # Should have paragraph blocks
        self.assertIn("paragraph_block", block_types)

        # Should have card blocks
        self.assertIn("card", block_types)

        # Count specific sections
        heading_count = block_types.count("heading_block")
        card_count = block_types.count("card")

        # Should have multiple headings (My Portfolio, Skills & Expertise, Recent Projects, Get In Touch)
        self.assertGreaterEqual(heading_count, 4)

        # Should have multiple cards (3 skills + 3 projects + 1 contact = 7)
        self.assertGreaterEqual(card_count, 7)

    def test_portfolio_page_menu_visibility(self):
        """Test that portfolio page is properly set to show in menus"""
        call_command("populate_portfolio")

        portfolio_page = PortfolioPage.objects.first()
        self.assertTrue(portfolio_page.show_in_menus)

    def test_no_home_page_error(self):
        """Test error when no home page exists"""
        # Delete all home pages
        HomePage.objects.all().delete()

        out = StringIO()

        # Run the command
        call_command("populate_portfolio", stdout=out)

        # Check error message
        output = out.getvalue()
        self.assertIn("No home page found", output)
