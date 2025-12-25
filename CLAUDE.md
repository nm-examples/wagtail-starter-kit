# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Wagtail CMS starter kit built with Django 5.2 and Wagtail 7.2. The project uses Docker for local development and includes a minimal frontend setup with Pico CSS (classless styling), SASS, and esbuild for JavaScript bundling.

## Development Environment

The project runs entirely in Docker containers. All Python/Django commands must be executed inside the Docker container using `make` commands or `docker exec`.

### Quick Start Commands

```bash
make quickstart    # Build containers, migrate, collect static, test, and run server
make superuser     # Create a superuser (run this separately after quickstart)
```

### Essential Development Commands

**Container Management:**
- `make build` - Build Docker containers
- `make up` - Start containers in detached mode
- `make down` - Stop and remove containers
- `make destroy` - Stop, remove containers and delete volumes
- `make restart` - Restart containers
- `make sh` - Open bash shell in app container
- `make run` - Start Django development server (localhost:8000)

**Database:**
- `make migrate` - Apply Django migrations
- `make superuser` - Create admin superuser

**Testing:**
- `make collectstatic` - Collect static files (required before running tests)
- `make test` - Run Django test suite

**Frontend Build:**
- `npm install` - Install Node dependencies
- `npm start` - Watch mode: compile SASS/JS and auto-reload on changes
- `npm run build` - Production build: minified and optimized assets
- `make frontend` - Install npm packages and build production assets
- `make start` - Install, build, and start frontend in watch mode

## Architecture

### Project Structure

```
app/                          # Django project root
├── settings/
│   ├── base.py              # Base settings (database, static files, Wagtail config)
│   ├── dev.py               # Development settings (DEBUG=True, browser reload)
│   └── production.py        # Production settings
├── home/                     # Main app with HomePage model
├── search/                   # Search functionality
├── style_guide/             # Style guide app (DEBUG mode only)
└── templates/               # Base templates

static_src/                   # Frontend source files
├── scss/                     # SASS stylesheets (Pico CSS)
├── js/                       # JavaScript source (esbuild)
└── img/                      # Source images

static_compiled/              # Compiled frontend assets (gitignored)
```

### Database Configuration

The project supports SQLite (default), MySQL, or PostgreSQL. Switch databases by editing the `Makefile` at line 4:

```makefile
# Uncomment the database you want to use:
DC = docker compose -f compose.yaml -f compose.sqlite3.override.yaml    # SQLite
# DC = docker compose -f compose.yaml -f compose.postgresql.override.yaml  # PostgreSQL
# DC = docker compose -f compose.yaml -f compose.mysql.override.yaml       # MySQL
```

After changing databases, rebuild containers and rerun migrations.

### Settings Architecture

- `app/settings/base.py` - Core settings; database selection via environment variables
- `app/settings/dev.py` - Adds `django_browser_reload`, style_guide app, DEBUG=True
- `app/settings/production.py` - Production configuration

Environment variable `DJANGO_SETTINGS_MODULE` controls which settings file is used (defaults to `app.settings.dev` in Docker).

### URL Routing

`app/urls.py` defines the URL structure:
- `/admin/` - Wagtail admin interface
- `/django-admin/` - Django admin
- `/search/` - Search functionality
- `/style-guide/` - Style guide (dev only)
- `/documents/` - Document serving
- All other routes handled by Wagtail's page serving

### Frontend Architecture

**Build Process:**
- SASS files in `static_src/scss/` compile to `static_compiled/css/`
- JavaScript in `static_src/js/app.js` bundles to `static_compiled/js/app.js`
- Images in `static_src/img/` copy to `static_compiled/img/`
- Uses esbuild for JS bundling (fast, modern)
- Uses dart-sass for SCSS compilation

**Static Files:**
- Development: Served directly by Django from `static_compiled/`
- Production: Collected to `static/` via `collectstatic`, uses ManifestStaticFilesStorage

**Auto-reload:**
- `django-browser-reload` middleware watches both backend and frontend changes in DEBUG mode

## Custom Management Commands

### create_sample_media

Creates sample images and documents for testing:

```bash
# Default: 75 images, 50 documents
docker exec -it wagtail-starter-kit-app-1 python manage.py create_sample_media

# Custom amounts
docker exec -it wagtail-starter-kit-app-1 python manage.py create_sample_media --images 20 --documents 10

# Clear existing and create new
docker exec -it wagtail-starter-kit-app-1 python manage.py create_sample_media --clear

# Delete all sample content
docker exec -it wagtail-starter-kit-app-1 python manage.py create_sample_media --reset
```

## Code Quality Tools

**Pre-commit hooks** (`.pre-commit-config.yaml`):
- `ruff` - Fast linter and formatter (replaces black, isort, and flake8)
- `pyupgrade` - Python 3.10+ syntax updates
- `django-upgrade` - Django 5.2 best practices

**Python version:** >= 3.10

**Dependency management:** Uses `uv` (optional). Export requirements with `make requirements`.

## Important Implementation Notes

### Wagtail Page Models

The starter has a minimal `HomePage` model in `app/home/models.py`. When creating new page types:
- Inherit from `wagtail.models.Page`
- Add content panels for field editing
- Templates go in `app/<appname>/templates/<appname>/`
- Run `make migrate` after model changes

### Static Files Workflow

1. Edit files in `static_src/`
2. Run `npm start` (development) or `npm run build` (production)
3. Compiled files appear in `static_compiled/`
4. For deployment, run `make collectstatic` to gather all static files

### Database Migrations

All migrations run inside Docker:
```bash
make sh  # Enter container
python manage.py makemigrations
exit
make migrate  # Apply migrations
```

### Docker Container Names

The main app container is named `wagtail-starter-kit-app-1`. For direct docker exec:
```bash
docker exec -it wagtail-starter-kit-app-1 python manage.py <command>
```

## Services Available in Development

- **Django app:** http://localhost:8000
- **Wagtail admin:** http://localhost:8000/admin
- **MailHog (email testing):** http://localhost:8025
- **Database management:** http://localhost:8080 (if using MySQL/PostgreSQL)
- **Style guide:** http://localhost:8000/style-guide/ (DEBUG mode only)

## Testing Strategy

1. Always run `make collectstatic` before `make test`
2. Tests are run inside the Docker container
3. Django's built-in test runner is used

## Common Workflows

### Adding a New Wagtail Page Type

1. Create model in appropriate app (or create new app)
2. Run migrations inside container
3. Create template in app's templates directory
4. Register in Wagtail admin if needed

### Making Frontend Changes

1. Start watch mode: `npm start`
2. Edit files in `static_src/`
3. Browser auto-reloads via django-browser-reload
4. Build for production: `npm run build`

### Switching Databases

1. Edit `Makefile` line 4 to uncomment desired database
2. Run `make build` to rebuild with new compose file
3. Run `make up && make migrate`
4. Recreate superuser: `make superuser`

### Deploying

1. Build production assets: `npm run build`
2. Collect static files: `make collectstatic`
3. Ensure `static_compiled/` is included (remove from `.gitignore` or build in CI/CD)
4. Set environment variables for production settings
5. Use production database (PostgreSQL/MySQL recommended)
