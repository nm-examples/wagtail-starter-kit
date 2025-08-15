from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Site

from app.blog.models import Author, BlogIndexPage, BlogPage, BlogTagIndexPage
from app.home.models import HomePage


class PopulateBlogTestCase(TestCase):
    def setUp(self):
        # Get or create the root page and site
        from wagtail.models import Page

        try:
            root = Page.objects.get(slug="root")
        except Page.DoesNotExist:
            root = Page.add_root(title="Root", slug="root")

        # Create a home page for testing
        self.home_page = HomePage(
            title="Test Home",
            slug="test-home",
        )
        root.add_child(instance=self.home_page)

        # Create site if it doesn't exist
        if not Site.objects.exists():
            Site.objects.create(
                hostname="localhost",
                port=8000,
                root_page=self.home_page,
                is_default_site=True,
            )

    def test_populate_blog_basic(self):
        """Test basic blog population"""
        out = StringIO()

        # Run the command
        call_command("populate_blog", "--posts", "3", "--authors", "2", stdout=out)

        # Check that content was created
        self.assertEqual(BlogIndexPage.objects.count(), 1)
        self.assertEqual(BlogTagIndexPage.objects.count(), 1)
        self.assertEqual(BlogPage.objects.count(), 3)
        self.assertEqual(Author.objects.count(), 2)

        # Check success message
        self.assertIn(
            "Successfully created blog structure with 3 posts and 2 authors",
            out.getvalue(),
        )

    def test_populate_blog_with_existing_authors(self):
        """Test that existing authors are reused"""
        # Create an existing author
        Author.objects.create(name="Existing Author")

        out = StringIO()

        # Run the command
        call_command("populate_blog", "--posts", "2", "--authors", "3", stdout=out)

        # Should still have only 1 author (the existing one)
        self.assertEqual(Author.objects.count(), 1)
        self.assertIn("Using 1 existing authors", out.getvalue())

    def test_populate_blog_clear_option(self):
        """Test the clear option functionality"""
        # Create some initial content
        call_command("populate_blog", "--posts", "2", "--authors", "1")

        # Verify initial content exists
        self.assertEqual(BlogPage.objects.count(), 2)

        out = StringIO()

        # Run with clear option - focus on testing the clear messages
        call_command(
            "populate_blog", "--clear", "--posts", "1", "--authors", "1", stdout=out
        )

        # Check that clear messages appeared
        output = out.getvalue()
        self.assertIn("Cleared existing blog index pages", output)
        self.assertIn("Cleared existing blog tag pages", output)
        self.assertIn("Cleared all authors", output)
        self.assertIn("Cleared all blog tags", output)

    def test_blog_post_structure(self):
        """Test that blog posts have proper structure and relationships"""
        call_command("populate_blog", "--posts", "2", "--authors", "2")

        blog_post = BlogPage.objects.first()

        # Check that the blog post has required fields
        self.assertTrue(blog_post.title)
        self.assertTrue(blog_post.intro)
        self.assertTrue(blog_post.body)
        self.assertTrue(blog_post.date)

        # Check that it has authors and tags
        self.assertTrue(blog_post.authors.exists())
        self.assertTrue(blog_post.tags.exists())

        # Check that it's a child of blog index
        blog_index = BlogIndexPage.objects.first()
        self.assertEqual(blog_post.get_parent().specific, blog_index)

    def test_blog_index_structure(self):
        """Test that blog index page is properly structured"""
        call_command("populate_blog", "--posts", "1", "--authors", "1")

        blog_index = BlogIndexPage.objects.first()
        home_page = HomePage.objects.first()

        # Check that blog index is a child of home page
        self.assertEqual(blog_index.get_parent().specific, home_page)
        self.assertEqual(blog_index.slug, "blog")
        self.assertTrue(blog_index.intro)
