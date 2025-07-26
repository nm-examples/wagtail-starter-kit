import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from wagtail.images.models import Image

from app.blog.models import (
    Author,
    BlogIndexPage,
    BlogPage,
    BlogPageGalleryImage,
    BlogTagIndexPage,
)
from app.home.models import HomePage


class Command(BaseCommand):
    help = (
        "Creates a complete blog structure with sample content including blog index pages, "
        "blog posts with unique titles, authors, tags, and gallery images. Can be run "
        "multiple times safely to add more content without conflicts."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--posts",
            type=int,
            default=10,
            help=(
                "Number of blog posts to create (default: 10). Each post will have "
                "unique titles, slugs, content, authors, and tags."
            ),
        )
        parser.add_argument(
            "--authors",
            type=int,
            default=3,
            help=(
                "Number of authors to create (default: 3). If authors already exist, "
                "they will be reused instead of creating new ones."
            ),
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help=(
                "Clear existing blog content (posts and index pages) before creating "
                "new content. Authors are preserved to maintain relationships."
            ),
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

            # Clear existing content if requested
            if options["clear"]:
                self.clear_blog_content()
                # Refresh home page from database after clearing content
                home_page.refresh_from_db()

            # Create or get blog index page
            blog_index = self.create_blog_index(home_page)

            # Create blog tag index page
            self.create_blog_tag_index(home_page)

            # Create sample authors
            authors = self.create_authors(options["authors"])

            # Create blog posts
            self.create_blog_posts(blog_index, authors, options["posts"])

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created blog structure with {options['posts']} posts "
                    f"and {len(authors)} authors"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

    def clear_blog_content(self):
        """Clear existing blog content"""
        # Delete blog posts first (children)
        blog_posts = BlogPage.objects.all()
        for post in blog_posts:
            post.delete()
        self.stdout.write("Cleared existing blog posts")

        # Then delete the index pages
        blog_indices = BlogIndexPage.objects.all()
        for index in blog_indices:
            index.delete()
        self.stdout.write("Cleared existing blog index pages")

        tag_indices = BlogTagIndexPage.objects.all()
        for tag_index in tag_indices:
            tag_index.delete()
        self.stdout.write("Cleared existing blog tag pages")

        # # Finally delete authors
        # Author.objects.all().delete()
        # self.stdout.write("Cleared existing authors")

    def create_blog_index(self, home_page):
        """Create or get the blog index page"""
        # Try to get existing blog index that's a child of home page
        blog_index = home_page.get_children().type(BlogIndexPage).first()

        if not blog_index:
            blog_index = BlogIndexPage(
                title="Blog",
                slug="blog",
                intro=(
                    "<p>Welcome to our blog! Here you'll find the latest news, "
                    "insights, and stories from our team.</p>"
                ),
            )
            home_page.add_child(instance=blog_index)
            blog_index.save_revision().publish()
            self.stdout.write("Created blog index page")
        else:
            self.stdout.write("Blog index page already exists")

        return blog_index

    def create_blog_tag_index(self, home_page):
        """Create or get the blog tag index page"""
        # Try to get existing blog tag index that's a child of home page
        tag_index = home_page.get_children().type(BlogTagIndexPage).first()

        if not tag_index:
            tag_index = BlogTagIndexPage(
                title="Blog Tags",
                slug="blog-tags",
            )
            home_page.add_child(instance=tag_index)
            tag_index.save_revision().publish()
            self.stdout.write("Created blog tag index page")
        else:
            self.stdout.write("Blog tag index page already exists")

        return tag_index

    def create_authors(self, num_authors):
        """Create sample authors"""
        existing_authors = Author.objects.all()
        if existing_authors.exists():
            self.stdout.write(f"Using {existing_authors.count()} existing authors")
            return list(existing_authors)

        author_names = [
            "Alice Johnson",
            "Bob Smith",
            "Carol Davis",
            "David Wilson",
            "Eva Brown",
            "Frank Miller",
            "Grace Lee",
            "Henry Taylor",
            "Ivy Chen",
            "Jack Thompson",
        ]

        authors = []
        available_images = list(Image.objects.all())

        for i in range(min(num_authors, len(author_names))):
            author = Author.objects.create(
                name=author_names[i],
                author_image=(
                    random.choice(available_images) if available_images else None
                ),
            )
            authors.append(author)

        self.stdout.write(f"Created {len(authors)} authors")
        return authors

    def create_blog_posts(self, blog_index, authors, num_posts):
        """Create sample blog posts"""

        # Sample blog post data
        post_topics = [
            "Getting Started with Wagtail CMS",
            "Building Modern Web Applications",
            "The Future of Content Management",
            "Django Development Best Practices",
            "Responsive Web Design Tips",
            "SEO Optimization Strategies",
            "User Experience Design Principles",
            "Digital Marketing Trends",
            "Web Performance Optimization",
            "Accessibility in Web Development",
            "Progressive Web Applications",
            "API Design and Development",
            "Database Optimization Techniques",
            "Security Best Practices",
            "DevOps and Deployment Strategies",
        ]

        blog_tags = [
            "wagtail",
            "django",
            "python",
            "web-development",
            "cms",
            "frontend",
            "backend",
            "design",
            "ux",
            "seo",
            "performance",
            "security",
            "api",
            "database",
            "devops",
        ]

        available_images = list(Image.objects.all())

        for i in range(num_posts):
            # Generate unique blog post content
            topic = post_topics[i % len(post_topics)]
            post_date = date.today() - timedelta(days=random.randint(1, 365))

            # Select random authors (1-3 authors per post)
            post_authors = random.sample(
                authors, k=random.randint(1, min(3, len(authors)))
            )

            # Select random tags (2-4 tags per post)
            post_tags = random.sample(blog_tags, k=random.randint(2, 4))

            # Generate unique title and slug using date and random number
            random_suffix = random.randint(100, 999)
            unique_title = f"{topic} - {post_date.strftime('%B %Y')} Edition"
            base_slug = topic.lower().replace(" ", "-").replace("'", "")
            unique_slug = f"{base_slug}-{post_date.strftime('%Y%m%d')}-{random_suffix}"

            # Ensure slug uniqueness by checking existing slugs
            existing_slugs = BlogPage.objects.filter(
                slug__startswith=base_slug
            ).values_list("slug", flat=True)

            counter = 1
            original_slug = unique_slug
            while unique_slug in existing_slugs:
                unique_slug = f"{original_slug}-{counter}"
                counter += 1

            intro = self.generate_intro(topic)
            body = self.generate_body(topic)

            # Create the blog post using create method instead of manual instantiation
            blog_post = blog_index.add_child(
                instance=BlogPage(
                    title=unique_title,
                    slug=unique_slug,
                    date=post_date,
                    intro=intro,
                    body=body,
                )
            )

            # Publish the page
            blog_post.save_revision().publish()

            # Add authors
            blog_post.authors.set(post_authors)

            # Add tags
            for tag in post_tags:
                blog_post.tags.add(tag)

            # Add gallery images (0-3 images per post)
            if available_images:
                num_images = random.randint(0, min(3, len(available_images)))
                selected_images = random.sample(available_images, k=num_images)

                for idx, image in enumerate(selected_images):
                    BlogPageGalleryImage.objects.create(
                        page=blog_post,
                        image=image,
                        caption=f"Image {idx + 1} for {blog_post.title}",
                    )

            blog_post.save()

        self.stdout.write(f"Created {num_posts} blog posts")

    def generate_intro(self, topic):
        """Generate sample introduction for blog post"""
        intros = {
            "Getting Started with Wagtail CMS": (
                "Learn the basics of Wagtail CMS and how to build your first "
                "content-driven website with this powerful Django-based platform."
            ),
            "Building Modern Web Applications": (
                "Explore the latest techniques and tools for creating responsive, "
                "scalable web applications that meet today's user expectations."
            ),
            "The Future of Content Management": (
                "Discover emerging trends in content management systems and how "
                "they're shaping the digital landscape."
            ),
            "Django Development Best Practices": (
                "Master the art of Django development with proven patterns, "
                "conventions, and techniques used by experienced developers."
            ),
            "Responsive Web Design Tips": (
                "Create websites that look great on any device with these essential "
                "responsive design principles and practical implementation tips."
            ),
        }
        return intros.get(
            topic,
            f"An in-depth look at {topic.lower()} and its practical applications "
            f"in modern web development.",
        )

    def generate_body(self, topic):
        """Generate sample body content for blog post"""
        return f"""
        <h3>Introduction</h3>
        <p>In this comprehensive guide, we'll explore <strong>{topic.lower()}</strong> and its
        importance in modern web development. Whether you're a beginner or an experienced developer,
        this article will provide valuable insights and practical examples.</p>

        <h3>Key Concepts</h3>
        <p>Understanding the fundamental concepts is crucial for success. We'll cover the most
        important aspects that every developer should know about this topic.</p>

        <ul>
            <li>Core principles and methodologies</li>
            <li>Best practices and common patterns</li>
            <li>Tools and frameworks that can help</li>
            <li>Real-world applications and use cases</li>
        </ul>

        <h3>Implementation Guide</h3>
        <p>Let's dive into the practical implementation details. This section provides step-by-step
        instructions and code examples to help you get started.</p>

        <p>The implementation process involves several key steps:</p>
        <ol>
            <li><strong>Planning and Setup</strong>: Prepare your development environment and plan
            your approach</li>
            <li><strong>Core Implementation</strong>: Build the main functionality following best
            practices</li>
            <li><strong>Testing and Optimization</strong>: Ensure your implementation works correctly
            and performs well</li>
            <li><strong>Deployment and Maintenance</strong>: Deploy your solution and keep it
            updated</li>
        </ol>

        <h3>Advanced Techniques</h3>
        <p>For those looking to take their skills to the next level, here are some advanced
        techniques and considerations that can make a significant difference in your projects.</p>

        <h3>Conclusion</h3>
        <p>By following the guidelines and best practices outlined in this article, you'll be
        well-equipped to tackle <strong>{topic.lower()}</strong> in your own projects. Remember to
        keep learning and stay updated with the latest developments in the field.</p>

        <p><em>Happy coding!</em></p>
        """.strip()
