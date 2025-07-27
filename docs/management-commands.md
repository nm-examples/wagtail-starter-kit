# Management Commands Documentation

This document provides detailed information about the custom Django management commands available in this Wagtail project.

## Table of Contents

- [create_sample_media](#create_sample_media)
- [populate_homepage](#populate_homepage)
- [populate_settings](#populate_settings)
- [populate_blog](#populate_blog)
- [Future Commands](#future-commands)

---

## create_sample_media

**Location**: `app/home/management/commands/create_sample_media.py`

**Purpose**: Creates sample images and documents (media files) for testing and demonstration purposes in your Wagtail CMS.

### Overview

The `create_sample_media` command generates realistic sample content including:

- **Dynamic Images**: Programmatically generated JPEG images with random colors, shapes, and text overlays
- **Text Documents**: Structured text files with realistic business content
- **ZIP Archives**: Compressed archives containing collections of documents with README files

This command is perfect for:
- Populating a new Wagtail site with test content
- Demonstrating media management features
- Testing search functionality with varied content
- Creating realistic data for development and staging environments

### Command Usage

```bash
# Basic usage (creates 75 images and 50 documents by default)
python manage.py create_sample_media

# Custom amounts
python manage.py create_sample_media --images 20 --documents 10

# Clear existing content and create new
python manage.py create_sample_media --clear --images 15 --documents 8

# Create content without ZIP archives
python manage.py create_sample_media --no-zip

# Only delete existing content (no new content created)
python manage.py create_sample_media --reset
```

### Command Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--images` | Integer | 75 | Number of sample images to create |
| `--documents` | Integer | 50 | Number of sample documents to create |
| `--clear` | Flag | False | Clear existing images and documents before creating new ones |
| `--no-zip` | Flag | False | Skip creating ZIP archives of the documents |
| `--reset` | Flag | False | Delete all existing images and documents without creating new ones |

### Content Details

#### Images
- **Formats**: JPEG with 85% quality
- **Sizes**: Multiple dimensions including landscape (800x600), portrait (600x800), banners (1200x400), squares (400x400), and standard (1024x768)
- **Visual Elements**: Random geometric shapes, lines, and color combinations
- **Text Overlay**: Truncated version of the image title
- **Titles**: Unique combinations using descriptive words, subjects, and random numbers
  - Example: `"Vibrant Abstract Art #749"`
  - Example: `"Modern Architecture - Technology #321"`

#### Documents
- **Format**: UTF-8 encoded text files (.txt)
- **Structure**: Professional document layout with headers, metadata, and sections
- **Content**: Realistic business document types including:
  - Project Reports
  - User Manuals
  - Technical Specifications
  - Meeting Notes
  - Policy Documents
  - Training Materials
  - Research Findings
  - Implementation Guides
  - Quality Assurance Checklists
  - Release Notes
- **Titles**: Unique combinations using modifiers, contexts, projects, and random numbers
  - Example: `"Strategic Project Report for Development Team #7549"`
  - Example: `"User Manual - Phoenix Initiative #3281"`

#### ZIP Archives
When not using `--no-zip`, the command creates:

1. **Complete Archive**: Contains all generated documents plus a README
2. **Themed Archives**: Smaller collections grouped by type:
   - Project Documentation Bundle
   - Technical Resources Collection
   - User Guides and Manuals

Each ZIP file includes:
- All relevant documents
- A README.txt file explaining the archive contents
- Proper file organization

### Command Examples

#### Creating a small test set
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py create_sample_media --images 5 --documents 3 --no-zip
```

#### Setting up a demo environment
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py create_sample_media --clear --images 25 --documents 15
```

#### Cleaning up all test content
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py create_sample_media --reset
```

---

## populate_homepage

**Location**: `app/home/management/commands/populate_homepage.py`

**Purpose**: Populates the existing home page with sample hero section and body content for testing and demonstration purposes. Automatically sets up hero images, text, call-to-action buttons, and links to other pages.

### Overview

The `populate_homepage` command sets up a complete home page with both hero section and body content. This is useful for:

- Setting up a new Wagtail site with a professional-looking homepage
- Demonstrating Wagtail's hero section functionality and rich text capabilities
- Providing a starting point for content editors
- Testing page layouts and styling with realistic content and media
- Showcasing call-to-action functionality with links to other pages

The generated content includes:

**Hero Section:**
- **Hero image** (randomly selected from media library if available)
- **Hero text** (customizable introduction message)
- **Call-to-action button** (customizable button text)
- **CTA link** (automatically links to blog index, portfolio, or other available pages)

**Body Content:**
- **Welcome message** with Wagtail introduction
- **Image embed** (different from hero image when possible)
- **Getting started guide** with admin links
- **Feature overview** of the starter kit
- **Next steps** for development

### Command Usage

```bash
# Basic usage (populates empty home page with default hero content)
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage

# Overwrite existing content
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage --overwrite

# Custom hero text and call-to-action
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage \
  --hero-text "Welcome to My Amazing Site" \
  --hero-cta "Start Exploring"

# Complete customization with overwrite
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage \
  --overwrite \
  --hero-text "Your Custom Message Here" \
  --hero-cta "Get Started Today"
```

### Command Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--overwrite` | Flag | False | Overwrite existing content if it already exists |
| `--hero-text` | String | "Welcome to Your Amazing Wagtail Site" | Custom hero text to display |
| `--hero-cta` | String | "Explore Our Content" | Custom call-to-action button text |

### Command Examples

#### Populate empty home page with defaults
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage
```

#### Replace existing content
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage --overwrite
```

#### Custom hero content for branding
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage \
  --hero-text "Welcome to ACME Corporation" \
  --hero-cta "Discover Our Solutions"
```

#### Complete setup with custom content
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage \
  --overwrite \
  --hero-text "Your Business, Elevated" \
  --hero-cta "Get Started Today"
```

---

## populate_settings

**Location**: `app/base/management/commands/populate_settings.py`

**Purpose**: Populates the NavigationSettings with sample social media URLs and FooterText with sample content for site-wide settings and branding.

### Overview

The `populate_settings` command sets up essential site-wide settings including:

- **NavigationSettings**: Social media URLs for LinkedIn, GitHub, and Mastodon that can be displayed in headers, footers, or navigation areas
- **FooterText**: Rich HTML content for site footer including copyright notices and branding

This command is useful for:
- Initial site setup with default social media links
- Establishing consistent footer content across the site
- Setting up branding and contact information
- Providing starting content for site-wide settings

### Command Usage

```bash
# Basic usage (uses default Wagtail/Torchbox URLs and copyright notice)
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings

# Custom social media URLs
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings \
  --linkedin "https://www.linkedin.com/company/yourcompany" \
  --github "https://github.com/yourorganization" \
  --mastodon "https://mastodon.social/@youraccount"

# Custom footer text with HTML
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings \
  --footer-text "<p>&copy; 2024 Your Company. All rights reserved. Built with <a href='https://wagtail.org/'>Wagtail</a>.</p>"

# Overwrite existing settings
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings --overwrite

# Full customization
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings \
  --overwrite \
  --linkedin "https://www.linkedin.com/company/mycompany" \
  --github "https://github.com/mycompany" \
  --mastodon "https://fosstodon.org/@mycompany" \
  --footer-text "<p>&copy; 2024 My Company. Built with love and <a href='https://wagtail.org/'>Wagtail</a>.</p>"
```

### Command Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--overwrite` | Flag | False | Overwrite existing settings if they already exist |
| `--linkedin` | String | `https://www.linkedin.com/company/torchbox` | LinkedIn company URL |
| `--github` | String | `https://github.com/wagtail/wagtail` | GitHub organization or user URL |
| `--mastodon` | String | `https://fosstodon.org/@wagtail` | Mastodon account URL |
| `--footer-text` | String | Default copyright with Wagtail link | Footer content (HTML allowed) |

### Settings Details

#### NavigationSettings
- **Model**: `BaseGenericSetting` (global site settings)
- **Fields**:
  - `linkedin_url`: LinkedIn company or personal profile URL
  - `github_url`: GitHub organization or user profile URL
  - `mastodon_url`: Mastodon account URL
- **Usage**: Can be accessed in templates via `settings.base.NavigationSettings`
- **Admin**: Editable through Wagtail admin under Settings

#### FooterText
- **Model**: `Snippet` with `DraftStateMixin`, `RevisionMixin`, `PreviewableMixin`
- **Fields**:
  - `body`: Rich text field supporting HTML content
- **Features**:
  - Draft/live states for content staging
  - Revision history for tracking changes
  - Preview functionality for content review
- **Usage**: Can be included in footer templates as a snippet
- **Admin**: Manageable through Wagtail admin under Snippets > Footer Text

### Command Examples

#### Basic setup for new site
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings
```

#### Setup with your organization's URLs
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings \
  --linkedin "https://www.linkedin.com/company/yourcompany" \
  --github "https://github.com/yourorg"
```

#### Update existing settings with new footer
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings \
  --overwrite \
  --footer-text "<p>&copy; 2024 Your Company Name. All rights reserved.</p>"
```

#### Complete customization
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_settings \
  --overwrite \
  --linkedin "https://www.linkedin.com/company/acme-corp" \
  --github "https://github.com/acme-corp" \
  --mastodon "https://mastodon.social/@acmecorp" \
  --footer-text "<p>&copy; 2024 ACME Corporation. Innovating since 1949. <a href='/privacy/'>Privacy Policy</a></p>"
```

---

## populate_blog

**Location**: `app/blog/management/commands/populate_blog.py`

**Purpose**: Creates a complete blog structure with sample blog posts, authors, and index pages for testing and demonstration purposes in your Wagtail CMS.

### Overview

The `populate_blog` command generates a fully functional blog section including:

- **Blog Index Page**: Main landing page for the blog section
- **Blog Tag Index Page**: Page for organizing and filtering blog posts by tags
- **Sample Authors**: Realistic author profiles with optional images
- **Blog Posts**: Rich content blog posts with unique titles, content, tags, and gallery images
- **Relationships**: Proper parent-child page relationships and many-to-many author associations

### Command Usage

```bash
# Basic usage (creates 10 posts and 3 authors by default)
python manage.py populate_blog

# Custom amounts
python manage.py populate_blog --posts 5 --authors 2

# Clear existing blog content and create new
python manage.py populate_blog --clear --posts 15 --authors 4

# Add more posts to existing blog (runs multiple times safely)
python manage.py populate_blog --posts 3
python manage.py populate_blog --posts 5
```

### Command Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--posts` | Integer | 10 | Number of blog posts to create |
| `--authors` | Integer | 3 | Number of authors to create (reuses existing authors if available) |
| `--clear` | Flag | False | Clear existing blog content before creating new content |

### Content Structure

#### Blog Posts
- **Topics**: 15 predefined topics covering web development, CMS, Django, design, SEO, security, and more
- **Unique Titles**: Format: `"{Topic} - {Month Year} Edition"` (e.g., "Building Modern Web Applications - March 2025 Edition")
- **Smart Slugs**: Format: `{topic-slug}-{YYYYMMDD}-{random-3-digits}` with collision detection
- **Rich Content**: Structured HTML with headings, paragraphs, lists, and emphasized text
- **Random Dates**: Posts dated within the last year with random distribution
- **Tags**: 2-4 relevant tags per post from: wagtail, django, python, web-development, cms, frontend, backend, design, ux, seo, performance, security, api, database, devops

#### Authors
- **Predefined Names**: 10 realistic author names (Alice Johnson, Bob Smith, etc.)
- **Image Assignment**: Random selection from available images in media library
- **Reuse Logic**: Existing authors are reused when command runs multiple times
- **Preserved on Clear**: Authors are preserved when using `--clear` flag (by design)

#### Page Structure
```
Home Page
├── Blog (BlogIndexPage)
│   ├── Blog Post 1 (BlogPage)
│   ├── Blog Post 2 (BlogPage)
│   └── ...
└── Blog Tags (BlogTagIndexPage)
```

### Command Examples

#### Set up initial blog
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_blog
```

#### Create a large blog for demo
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_blog --clear --posts 25 --authors 5
```

#### Add more content to existing blog
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_blog --posts 8
```

#### Reset and start fresh
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_blog --clear --posts 12 --authors 3
```

---

## Future Commands

This section will be expanded as additional management commands are added to the project.
