# Management Commands Documentation

This document provides detailed information about the custom Django management commands available in this Wagtail project.

## Table of Contents

- [populate_homepage](#populate_homepage)
- [create_sample_media](#create_sample_media)
- [Future Commands](#future-commands)

---

## populate_homepage

**Location**: `app/home/management/commands/populate_homepage.py`

**Purpose**: Populates the existing home page with sample body content for testing and demonstration purposes. If images exist in the media library, one will be randomly selected and included in the content.

### Description

The `populate_homepage` command adds rich HTML content to the body field of your site's home page. This is useful for:

- Setting up a new Wagtail site with meaningful placeholder content
- Demonstrating Wagtail's rich text editing capabilities including image embeds
- Providing a starting point for content editors
- Testing page layouts and styling with realistic content and media

The generated content includes:

- **Welcome message** with Wagtail introduction
- **Random image embed** (if images are available in the media library)
- **Getting started guide** with admin links
- **Feature overview** of the starter kit
- **Next steps** for development

### Usage

```bash
# Basic usage (populates empty home page)
python manage.py populate_homepage

# Overwrite existing content
python manage.py populate_homepage --overwrite
```

### Options

| Option | Description |
|--------|-------------|
| `--overwrite` | Overwrite existing body content if it already exists |

### Examples

#### Populate empty home page
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage
```

#### Replace existing content
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py populate_homepage --overwrite
```

### Technical Implementation

- Uses Django's management command framework
- Safely updates the HomePage model via Django ORM
- Automatically selects a random image from the media library if available
- Embeds images using Wagtail's rich text embed format
- Creates a new revision and publishes it to track the change
- Provides clear feedback on success/failure states and image selection
- Handles cases where no home page exists or no images are available

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

### Implementation Details

#### Dependencies
- **PIL (Pillow)**: For dynamic image generation
- **zipfile**: For creating compressed archives
- **Wagtail**: Uses `wagtail.images.models.Image` and `wagtail.documents.models.Document`

---

## Future Commands

This section will be expanded as additional management commands are added to the project.
