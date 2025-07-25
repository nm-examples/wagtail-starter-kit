import io
import random
import string
import zipfile

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image as PILImage
from PIL import ImageDraw
from wagtail.documents.models import Document
from wagtail.images.models import Image


class Command(BaseCommand):
    help = "Creates sample images and documents (media files) for testing purposes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--images",
            type=int,
            default=75,
            help="Number of sample images to create (default: 75)",
        )
        parser.add_argument(
            "--documents",
            type=int,
            default=50,
            help="Number of sample documents to create (default: 5)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing images and documents before creating new ones",
        )
        parser.add_argument(
            "--no-zip",
            action="store_true",
            help="Skip creating ZIP archives of the documents",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all existing images and documents without creating new ones",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write(
                "Resetting: Deleting all existing images and documents..."
            )
            image_count = Image.objects.count()
            document_count = Document.objects.count()

            Image.objects.all().delete()
            Document.objects.all().delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Reset complete: Deleted {image_count} images and {document_count} documents"
                )
            )
            return  # Exit early without creating new content

        if options["clear"]:
            self.stdout.write("Clearing existing images and documents...")
            Image.objects.all().delete()
            Document.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared existing content."))

        # Create sample images
        self.create_sample_images(options["images"])

        # Create sample documents
        self.create_sample_documents(
            options["documents"], create_zip=not options["no_zip"]
        )

        zip_msg = " and ZIP archives" if not options["no_zip"] else ""
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {options["images"]} images, {options["documents"]} documents{zip_msg}'
            )
        )

    def create_sample_images(self, count):
        """Create sample images with different sizes and colors"""
        self.stdout.write(f"Creating {count} sample images...")

        image_titles = [
            "Beautiful Landscape",
            "Abstract Art",
            "Modern Architecture",
            "City Skyline",
            "Natural Wonder",
            "Artistic Portrait",
            "Geometric Pattern",
            "Vintage Design",
            "Creative Concept",
            "Colorful Composition",
            "Minimalist Design",
            "Dynamic Scene",
            "Peaceful Setting",
            "Bold Statement",
            "Elegant Style",
        ]

        # Random descriptive words to make titles more unique
        descriptive_words = [
            "Vibrant",
            "Serene",
            "Bold",
            "Subtle",
            "Dramatic",
            "Gentle",
            "Striking",
            "Ethereal",
            "Rustic",
            "Contemporary",
            "Classic",
            "Innovative",
            "Timeless",
            "Refined",
            "Organic",
            "Geometric",
            "Fluid",
            "Sharp",
            "Soft",
            "Intense",
            "Delicate",
            "Powerful",
            "Mystical",
            "Urban",
            "Natural",
            "Industrial",
            "Artistic",
            "Photographic",
            "Digital",
            "Handcrafted",
            "Professional",
        ]

        # Random subjects/themes
        subjects = [
            "Sunset",
            "Ocean",
            "Mountain",
            "Forest",
            "Building",
            "Street",
            "Garden",
            "Studio",
            "Gallery",
            "Workshop",
            "Landscape",
            "Portrait",
            "Still Life",
            "Architecture",
            "Nature",
            "Technology",
            "Fashion",
            "Travel",
            "Culture",
            "Business",
            "Event",
            "Celebration",
            "Season",
            "Weather",
            "Light",
        ]

        colors = [
            (255, 99, 132),  # Red
            (54, 162, 235),  # Blue
            (255, 205, 86),  # Yellow
            (75, 192, 192),  # Teal
            (153, 102, 255),  # Purple
            (255, 159, 64),  # Orange
            (199, 199, 199),  # Grey
            (83, 102, 255),  # Indigo
            (255, 99, 255),  # Pink
            (99, 255, 132),  # Green
        ]

        sizes = [
            (800, 600),  # Landscape
            (600, 800),  # Portrait
            (1200, 400),  # Wide banner
            (400, 400),  # Square
            (1024, 768),  # Standard
        ]

        for i in range(count):
            # Create a dynamic image
            width, height = random.choice(sizes)
            color = random.choice(colors)

            # Create image with PIL
            img = PILImage.new("RGB", (width, height), color)
            draw = ImageDraw.Draw(img)

            # Add some visual elements
            # Draw some random shapes
            for _ in range(random.randint(3, 8)):
                shape_type = random.choice(["rectangle", "ellipse", "line"])
                shape_color = tuple(random.randint(0, 255) for _ in range(3))

                if shape_type == "rectangle":
                    x1, y1 = random.randint(0, width // 2), random.randint(
                        0, height // 2
                    )
                    x2, y2 = random.randint(x1, width), random.randint(y1, height)
                    draw.rectangle([x1, y1, x2, y2], fill=shape_color, outline=None)
                elif shape_type == "ellipse":
                    x1, y1 = random.randint(0, width // 2), random.randint(
                        0, height // 2
                    )
                    x2, y2 = random.randint(x1, width), random.randint(y1, height)
                    draw.ellipse([x1, y1, x2, y2], fill=shape_color, outline=None)
                else:  # line
                    x1, y1 = random.randint(0, width), random.randint(0, height)
                    x2, y2 = random.randint(0, width), random.randint(0, height)
                    draw.line(
                        [x1, y1, x2, y2], fill=shape_color, width=random.randint(2, 10)
                    )

            # Create unique title with random descriptive elements
            base_title = random.choice(image_titles)
            descriptive = random.choice(descriptive_words)
            subject = random.choice(subjects)
            random_number = random.randint(100, 999)  # 3-digit random number

            # Randomly choose different title formats for variety
            title_formats = [
                f"{descriptive} {base_title} #{random_number}",
                f"{base_title} - {subject} #{random_number}",
                f"{descriptive} {subject} {base_title} #{random_number}",
                f"{base_title} in {subject} #{random_number}",
                f"{subject}: {descriptive} {base_title} #{random_number}",
            ]

            unique_title = random.choice(title_formats)

            try:
                # Try to use a default font, fallback to default if not available
                draw.text(
                    (20, 20),
                    unique_title[:20],
                    fill=(255, 255, 255),
                    stroke_fill=(0, 0, 0),
                    stroke_width=2,
                )
            except Exception:
                # Fallback without font
                draw.text((20, 20), unique_title[:20], fill=(255, 255, 255))

            # Save image to BytesIO
            img_io = io.BytesIO()
            img.save(img_io, format="JPEG", quality=85)
            img_io.seek(0)

            # Create Wagtail Image with unique title
            filename = f"sample_image_{i+1}_{slugify(unique_title)}.jpg"
            image = Image(
                title=unique_title, file=ContentFile(img_io.getvalue(), name=filename)
            )
            image.save()

            self.stdout.write(f"  Created image: {image.title}")

    def create_sample_documents(self, count, create_zip=True):
        """Create sample documents (text files) and optionally ZIP archives"""
        self.stdout.write(f"Creating {count} sample documents...")

        document_types = [
            {
                "title": "Project Report",
                "content": (
                    "This is a comprehensive project report detailing the progress "
                    "and outcomes of our latest initiative."
                ),
            },
            {
                "title": "User Manual",
                "content": (
                    "Step-by-step instructions for using our application "
                    "effectively and efficiently."
                ),
            },
            {
                "title": "Technical Specification",
                "content": (
                    "Detailed technical specifications and requirements "
                    "for the development team."
                ),
            },
            {
                "title": "Meeting Notes",
                "content": (
                    "Summary of key points and action items from our "
                    "weekly team meeting."
                ),
            },
            {
                "title": "Policy Document",
                "content": (
                    "Official company policy regarding data handling "
                    "and security procedures."
                ),
            },
            {
                "title": "Training Material",
                "content": (
                    "Educational content designed to help new team members "
                    "get up to speed."
                ),
            },
            {
                "title": "Research Findings",
                "content": (
                    "Analysis and conclusions from our market research "
                    "and user studies."
                ),
            },
            {
                "title": "Implementation Guide",
                "content": (
                    "Comprehensive guide for implementing new features "
                    "and functionality."
                ),
            },
            {
                "title": "Quality Assurance Checklist",
                "content": (
                    "Detailed checklist to ensure quality standards are met "
                    "throughout the process."
                ),
            },
            {
                "title": "Release Notes",
                "content": (
                    "Documentation of new features, improvements, and bug fixes "
                    "in the latest release."
                ),
            },
        ]

        # Random modifiers to make document titles more unique
        document_modifiers = [
            "Comprehensive",
            "Detailed",
            "Complete",
            "Essential",
            "Advanced",
            "Basic",
            "Updated",
            "Revised",
            "Final",
            "Draft",
            "Preliminary",
            "Executive",
            "Strategic",
            "Operational",
            "Technical",
            "Business",
            "Internal",
            "External",
            "Annual",
            "Quarterly",
            "Monthly",
            "Weekly",
            "Emergency",
            "Standard",
        ]

        # Random contexts/departments
        contexts = [
            "Development Team",
            "Marketing Department",
            "Sales Division",
            "HR Department",
            "Finance Team",
            "Operations Group",
            "Executive Committee",
            "Board of Directors",
            "Product Team",
            "Design Team",
            "Engineering Group",
            "Customer Success",
            "Quality Assurance",
            "Project Management",
            "IT Department",
            "Legal Team",
            "Compliance Office",
            "Research Team",
            "Analytics Group",
            "Security Team",
        ]

        # Random project/product names
        project_names = [
            "Phoenix",
            "Atlas",
            "Horizon",
            "Summit",
            "Catalyst",
            "Nexus",
            "Vertex",
            "Prism",
            "Zenith",
            "Matrix",
            "Pulse",
            "Orbit",
            "Stellar",
            "Quantum",
            "Fusion",
            "Digital",
            "Cloud",
            "Mobile",
            "Web",
            "API",
            "Platform",
            "System",
            "Framework",
            "Solution",
            "Initiative",
            "Program",
            "Phase",
        ]

        # Store created documents for ZIP creation
        created_docs = []

        for i in range(count):
            doc_info = random.choice(document_types)

            # Create unique title with random elements
            base_title = doc_info["title"]
            modifier = random.choice(document_modifiers)
            context = random.choice(contexts)
            project = random.choice(project_names)
            random_number = random.randint(
                1000, 9999
            )  # 4-digit random number for documents

            # Randomly choose different title formats for variety
            title_formats = [
                f"{modifier} {base_title} #{random_number}",
                f"{base_title} - {project} Project #{random_number}",
                f"{context}: {base_title} #{random_number}",
                f"{project} {base_title} #{random_number}",
                f"{modifier} {base_title} for {context} #{random_number}",
                f"{base_title} ({project} Initiative) #{random_number}",
                f"{context} {modifier} {base_title} #{random_number}",
            ]

            unique_title = random.choice(title_formats)

            # Create content with more detail
            content = f"""
{unique_title}
{'=' * len(unique_title)}

Date: {self.get_random_date()}
Author: Sample Author {i+1}
Version: 1.{i}
Department: {context}
Project: {project}

Overview
--------
{doc_info['content']}

This document contains important information that has been generated automatically
for demonstration purposes. In a real-world scenario, this would contain actual
business content, specifications, or documentation relevant to your project.

Key Points:
- Point 1: Comprehensive coverage of the topic
- Point 2: Clear and actionable information
- Point 3: Well-structured and easy to follow
- Point 4: Relevant examples and use cases

Additional Details
------------------
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris.

Conclusion
----------
This document serves as a valuable resource for understanding the topic at hand
and provides actionable insights for implementation.

Document ID: DOC-{str(i+1).zfill(3)}
Classification: Public
"""

            # Create text file
            filename = f"{slugify(unique_title)}_{i+1}.txt"

            # Convert content to bytes
            content_bytes = content.encode("utf-8")

            # Store for ZIP creation
            created_docs.append(
                {"filename": filename, "content": content_bytes, "title": unique_title}
            )

            # Create Wagtail Document with unique title
            document = Document(
                title=unique_title, file=ContentFile(content_bytes, name=filename)
            )
            document.save()

            self.stdout.write(f"  Created document: {document.title}")

        # Create ZIP archives if requested
        if create_zip and created_docs:
            self.create_zip_archives(created_docs, count)

    def create_zip_archives(self, documents, base_count):
        """Create ZIP archives containing the text documents"""
        self.stdout.write("Creating ZIP archives...")

        # Create individual ZIP files (group documents)
        zip_groups = [
            {
                "name": "project_documentation",
                "description": "Project Documentation Bundle",
            },
            {
                "name": "technical_resources",
                "description": "Technical Resources Collection",
            },
            {"name": "user_guides", "description": "User Guides and Manuals"},
        ]

        # Create one comprehensive ZIP with all documents
        all_docs_zip = io.BytesIO()
        with zipfile.ZipFile(all_docs_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add a README file to the ZIP
            readme_content = f"""
Document Archive
================

This archive contains {len(documents)} sample documents created for demonstration purposes.

Contents:
---------
"""
            for doc in documents:
                readme_content += f"- {doc['filename']}: {doc['title']}\n"

            readme_content += f"""
Created: {self.get_random_date()}
Archive Type: Complete Documentation Set
Total Files: {len(documents)}

These documents are generated samples and can be used for testing
document management systems, search functionality, and user interfaces.
"""

            zipf.writestr("README.txt", readme_content.encode("utf-8"))

            # Add all documents to the ZIP
            for doc in documents:
                zipf.writestr(doc["filename"], doc["content"])

        all_docs_zip.seek(0)

        # Create the comprehensive ZIP document
        zip_document = Document(
            title=f"Complete Document Archive ({len(documents)} files)",
            file=ContentFile(
                all_docs_zip.getvalue(),
                name=f"document_archive_{len(documents)}_files.zip",
            ),
        )
        zip_document.save()
        self.stdout.write(f"  Created ZIP archive: {zip_document.title}")

        # Create smaller themed ZIP files
        docs_per_zip = max(1, len(documents) // len(zip_groups))

        for i, zip_info in enumerate(zip_groups):
            if i * docs_per_zip >= len(documents):
                break

            start_idx = i * docs_per_zip
            end_idx = min((i + 1) * docs_per_zip, len(documents))
            zip_docs = documents[start_idx:end_idx]

            if not zip_docs:
                continue

            themed_zip = io.BytesIO()
            with zipfile.ZipFile(themed_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add a themed README
                themed_readme = f"""
{zip_info['description']}
{'=' * len(zip_info['description'])}

This themed archive contains {len(zip_docs)} documents related to {zip_info['description'].lower()}.

Contents:
---------
"""
                for doc in zip_docs:
                    themed_readme += f"- {doc['filename']}: {doc['title']}\n"

                themed_readme += f"""
Created: {self.get_random_date()}
Theme: {zip_info['description']}
Files: {len(zip_docs)}
"""

                zipf.writestr("README.txt", themed_readme.encode("utf-8"))

                # Add documents to themed ZIP
                for doc in zip_docs:
                    zipf.writestr(doc["filename"], doc["content"])

            themed_zip.seek(0)

            # Create themed ZIP document
            themed_zip_document = Document(
                title=f"{zip_info['description']} ({len(zip_docs)} files)",
                file=ContentFile(themed_zip.getvalue(), name=f"{zip_info['name']}.zip"),
            )
            themed_zip_document.save()
            self.stdout.write(f"  Created themed ZIP: {themed_zip_document.title}")

    def get_random_date(self):
        """Generate a random date string"""
        import datetime
        import random

        start_date = datetime.date(2024, 1, 1)
        end_date = datetime.date.today()

        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)

        random_date = start_date + datetime.timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")

    def generate_random_string(self, length=8):
        """Generate a random string for unique identifiers"""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
