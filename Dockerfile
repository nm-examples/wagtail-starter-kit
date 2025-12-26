FROM node:20

COPY package.json package-lock.json ./
RUN npm install

COPY ./static_src/ ./static_src/
COPY ./scripts/ ./scripts/
RUN npm run build

# Use the uv image (slim) with Python 3.10 on Debian bookworm.
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# Sets the database module to be used, if not using SQLite.
ARG DBMODULE

# Add user that will be used in the container.
RUN useradd -m wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DBMODULE=${DBMODULE}

# Install runtime system libraries required by Wagtail/Django and Pillow.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    zlib1g \
    libwebp7 \
 && rm -rf /var/lib/apt/lists/*

# Prepare app workspace and install Python deps using uv from pyproject.
WORKDIR /app
COPY pyproject.toml uv.lock ./
ENV UV_NO_DEV=1 \
    UV_LINK_MODE=copy
ENV UV_PYTHON_CACHE_DIR=/root/.cache/uv/python

# Temporarily install build tools and headers to allow building wheels, then purge.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev
RUN --mount=type=cache,target=/root/.cache/uv \
    uv python install
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Remove build-only packages to slim the final image.
RUN apt-get purge --yes --quiet \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && apt-get autoremove --yes --quiet --purge \
 && rm -rf /var/lib/apt/lists/*

# Ensure the container uses the project virtualenv at runtime.
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Optional DB driver installation (kept for compatibility with existing compose overrides).
RUN ${DBMODULE}

# Use /app folder as a directory where the source code is stored.
COPY --from=0 ./static_compiled ./static_compiled

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown -R wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files using the project environment.
RUN uv run python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
# CMD set -xe; python manage.py migrate --noinput; gunicorn app.wsgi:application
