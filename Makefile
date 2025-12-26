# Makefile for Docker Compose commands

# Default Docker image name for direct builds
IMAGE_NAME ?= wagtail-starter-kit

# --- Un-comment based on the database you want to use --- #
DC = docker compose -f compose.yaml -f compose.sqlite3.override.yaml # SQLITE Database
# DC = docker compose -f compose.yaml -f compose.postgresql.override.yaml # PostgreSQL Database
# DC = docker compose -f compose.yaml -f compose.mysql.override.yaml # MySQL Database
# --- #

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Docker Compose commands"
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
	@echo " quickstart     Build, start, and run the containers (npm & docker)"
	@echo " requirements   Export requirements.txt (uv)"
	@echo " docker-size    Show the size of the Docker image $(IMAGE_NAME)"
	@echo " docker-build-size  Build the Docker image and show its size"
	@echo " docker-prune   Remove unused Docker data (images, containers, networks)"
	@echo "                 Add WITH_VOLUMES=1 to include volumes"
	@echo " docker-prune-all  Remove unused Docker data including volumes"
	@echo " clean          Clean up generated files and folders (node_modules, static, media, etc.)"
	@echo " frontend       Build the frontend (npm)"
	@echo " start          Build the front end and start local development server (npm)"
	@echo ""

# Build the containers
.PHONY: build
build:
	$(DC) build

# Start the containers
.PHONY: up
up:
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

# Export requirements.txt
.PHONY: requirements
requirements:
	uv export --no-hashes --no-dev --output-file requirements.txt --locked

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
