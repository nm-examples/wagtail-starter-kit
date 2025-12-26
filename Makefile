# Makefile for Docker Compose commands

# Load .env so we can switch database without editing this file
include .env

# Default Docker image name for direct builds
IMAGE_NAME ?= wagtail-starter-kit

# Determine which compose override to use based on DATABASE env var
# Allowed values: sqlite (default), postgres, mysql
ifeq ($(DATABASE),postgres)
COMPOSE_DB_FILE := compose.postgresql.override.yaml
else ifeq ($(DATABASE),mysql)
COMPOSE_DB_FILE := compose.mysql.override.yaml
else
COMPOSE_DB_FILE := compose.sqlite3.override.yaml
endif

DC = docker compose -f compose.yaml -f $(COMPOSE_DB_FILE)

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Docker Compose commands (DATABASE=$(DATABASE) -> $(COMPOSE_DB_FILE))"
	@echo " build          Build the Docker containers"
	@echo " up             Start the Docker containers"
	@echo " down           Stop and remove the Docker containers"
	@echo " destroy        Stop and remove the Docker containers, networks, and volumes"
	@echo " run            Run the Django development server"
	@echo ""
	@echo "Container commands"
	@echo " migrate        Run Django migrations"
	@echo " superuser      Create a superuser"
	@echo " restoredb      Restore the database from a backup"
	@echo " sh             Execute a command in a running container"
	@echo " restart        Restart the containers"
	@echo ""
	@echo "Miscellaneous"
	@echo " check-env      Validate required .env variables for selected database"
	@echo " quickstart     Build, start, and run the containers (npm & docker)"
	@echo " docker-size    Show the size of the Docker image $(IMAGE_NAME)"
	@echo " docker-build-size  Build the Docker image and show its size"
	@echo " docker-prune   Remove unused Docker data (images, containers, networks)"
	@echo "                 Add WITH_VOLUMES=1 to include volumes"
	@echo " docker-prune-all  Remove unused Docker data including volumes"
	@echo " clean          Clean up generated files and folders (node_modules, static, media, etc.)"
	@echo " frontend       Build the frontend (npm)"
	@echo " start          Build the front end and start local development server (npm)"
	@echo ""

# Required env variables
REQUIRED_COMMON := DJANGO_ALLOWED_HOSTS DJANGO_SECRET_KEY WAGTAIL_SITE_NAME WAGTAILADMIN_BASE_URL
ifeq ($(DATABASE),postgres)
REQUIRED_DB := POSTGRES_HOST POSTGRES_PORT POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD
else ifeq ($(DATABASE),mysql)
REQUIRED_DB := MYSQL_HOST MYSQL_PORT MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD MYSQL_ROOT_PASSWORD MYSQL_ROOT_HOST
else
REQUIRED_DB :=
endif

.PHONY: check-env
check-env:
	@if [ ! -f .env ]; then \
	  echo "Missing .env. Copy .env.example to .env and set required values."; \
	  exit 1; \
	fi; \
	set -a; . ./.env; set +a; \
	missing=0; \
	for v in $(REQUIRED_COMMON) $(REQUIRED_DB); do \
	  val=$$(printenv $$v); \
	  if [ -z "$$val" ]; then \
	    echo "Missing required env var: $$v"; \
	    missing=1; \
	  fi; \
	done; \
	if [ $$missing -ne 0 ]; then \
	  echo "\nSet the missing variables in .env (DATABASE=$(DATABASE))."; \
	  exit 1; \
	else \
	  echo "Environment OK for DATABASE=$(DATABASE)"; \
	fi

# Build the containers
.PHONY: build
build: check-env
	$(DC) build

# Start the containers
.PHONY: up
up: check-env
	$(DC) up -d

# Stop and remove containers, networks, and volumes
.PHONY: down
down:
	$(DC) down

# Restart the containers
.PHONY: restart
restart:
	$(DC) restart

# Execute a command in a running container
.PHONY: sh
sh:
	$(DC) exec app bash

# Run the Django development server
.PHONY: run
run:
	$(DC) exec app python manage.py runserver 0.0.0.0:8000

# Stop and remove the Docker containers, networks, and volumes
.PHONY: destroy
destroy:
	$(DC) down -v

# Run migrations
.PHONY: migrate
migrate:
	$(DC) exec app python manage.py migrate

# Create a superuser
.PHONY: superuser
superuser:
	$(DC) exec app python manage.py createsuperuser

# Collect static files
.PHONY: collectstatic
collectstatic:
	$(DC) exec app python manage.py collectstatic --noinput

# Run tests, you will need to have run `make collectstatic` first
.PHONY: test
test:
	$(DC) exec app python manage.py test

# Quickstart
.PHONY: quickstart
quickstart: frontend build up migrate collectstatic test run

# Build the fontend
.PHONY: frontend
frontend:
	npm install
	npm run build

# Start the frontend and run the local development server
.PHONY: start
start:
	npm install
	npm run build
	npm run start

# Show the size of the built Docker image
.PHONY: docker-size
docker-size:
	@docker image ls $(IMAGE_NAME) --format '{{.Repository}}:{{.Tag}} {{.Size}}' | sed -n '1p' || (echo "Image not found: $(IMAGE_NAME)" && exit 1)

# Build the Docker image directly and print its size
.PHONY: docker-build-size
docker-build-size:
	docker build -t $(IMAGE_NAME) .
	@docker image ls $(IMAGE_NAME) --format '{{.Repository}}:{{.Tag}} {{.Size}}' | sed -n '1p'

# Prune unused Docker resources
.PHONY: docker-prune
docker-prune:
	@if [ "$(WITH_VOLUMES)" = "1" ]; then \
		echo "Pruning unused Docker data (including volumes)"; \
		docker system prune -f --volumes; \
	else \
		echo "Pruning unused Docker data (images, containers, networks)"; \
		docker system prune -f; \
	fi

# Always prune including volumes
.PHONY: docker-prune-all
docker-prune-all:
	@echo "Pruning unused Docker data (including volumes)"
	docker system prune -f --volumes

# Clean up
.PHONY: clean
clean:
	@echo "This will remove all generated files and folders (node_modules, static, media + db.sqlite3)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf ./node_modules ./static ./static_compiled ./media db.sqlite3; \
	fi
