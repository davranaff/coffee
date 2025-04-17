# Makefile for Coffee Shop API project

# Mark all targets that are not files
.PHONY: help setup env db migrate migration downgrade migrate-status run run-prod test test-cov docker-build docker-up docker-down clean lint format install-deps update-deps

# Variables
PYTHON = python3
PIP = $(PYTHON) -m pip
PYTEST = pytest
ALEMBIC = alembic
DOCKER = docker
DOCKER_COMPOSE = docker-compose
FLAKE8 = flake8
BLACK = black
ISORT = isort

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m  # No Color

# Main help command with description of all targets
help:
	@echo "Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  setup          Full project setup (create .env, databases, migrations)"
	@echo "  env            Create .env file from template"
	@echo "  db             Create main and test databases"
	@echo "  install-deps   Install dependencies from requirements.txt"
	@echo "  update-deps    Update dependencies"
	@echo ""
	@echo "Database and migrations:"
	@echo "  migrate        Apply all migrations"
	@echo "  migration m=   Create new migration (specify message: m=\"Description\")"
	@echo "  downgrade      Rollback one migration"
	@echo "  migrate-status Show migrations status"
	@echo ""
	@echo "Run server:"
	@echo "  run            Run development server"
	@echo "  run-prod       Run production server"
	@echo ""
	@echo "Testing and code quality:"
	@echo "  test           Run all tests"
	@echo "  test-cov       Run tests with coverage report"
	@echo "  lint           Check code with linter (flake8)"
	@echo "  format         Format code (black + isort)"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-up      Start containers with Docker Compose"
	@echo "  docker-down    Stop Docker Compose containers"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          Remove temporary files and caches"
	@echo ""

# Project setup
setup: env install-deps db migrate
	@echo "${GREEN}✅ Project setup completed${NC}"

# Install dependencies
install-deps:
	@echo "📦 Installing dependencies..."
	@$(PIP) install -r requirements.txt
	@echo "${GREEN}✅ Dependencies installed${NC}"

# Update dependencies
update-deps:
	@echo "🔄 Updating dependencies..."
	@$(PIP) install --upgrade -r requirements.txt
	@echo "${GREEN}✅ Dependencies updated${NC}"

# Create .env file from template
env:
	@if [ ! -f .env ]; then \
		echo "📄 Creating .env file from template..."; \
		cp .env.example .env; \
		echo "${GREEN}✅ .env file created${NC}"; \
	else \
		echo "${YELLOW}🔄 .env file already exists${NC}"; \
	fi

# Create databases
db:
	@echo "🗃️  Creating databases..."
	@$(PYTHON) setup_project.py --db
	@echo "${GREEN}✅ Databases created${NC}"

# Migrations
migrate:
	@echo "🔄 Applying migrations..."
	@$(ALEMBIC) upgrade head
	@echo "${GREEN}✅ Migrations applied${NC}"

# Create new migration
migration:
	@if [ -z "$(m)" ]; then \
		echo "${YELLOW}❌ Please specify migration message: make migration m=\"Migration description\"${NC}"; \
		exit 1; \
	fi
	@echo "📝 Creating migration: $(m)..."
	@$(ALEMBIC) revision --autogenerate -m "$(m)"
	@echo "${GREEN}✅ Migration created${NC}"

# Rollback migration
downgrade:
	@echo "⏮️  Rolling back migration..."
	@$(ALEMBIC) downgrade -1
	@echo "${GREEN}✅ Migration reverted${NC}"

# Migrations status
migrate-status:
	@echo "🔍 Migrations status:"
	@$(ALEMBIC) current

# Run server
run:
	@echo "🚀 Starting development server..."
	@uvicorn app.main:app --reload

# Run server in production mode
run-prod:
	@echo "🚀 Starting production server..."
	@uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

# Testing
test:
	@echo "🧪 Running tests..."
	@$(PYTEST)
	@echo "${GREEN}✅ Tests completed${NC}"

# Testing with coverage report
test-cov:
	@echo "🧪 Running tests with coverage report..."
	@$(PYTEST) --cov=app --cov-report=term-missing
	@echo "${GREEN}✅ Tests with coverage report completed${NC}"

# Linter check
lint:
	@echo "🔍 Checking code with linter..."
	@$(FLAKE8) app tests
	@echo "${GREEN}✅ Check completed${NC}"

# Code formatting
format:
	@echo "🎨 Formatting code..."
	@$(ISORT) app tests
	@$(BLACK) app tests
	@echo "${GREEN}✅ Code formatted${NC}"

# Docker
docker-build:
	@echo "🔨 Building Docker image..."
	@$(DOCKER) build -t coffee-shop-api .
	@echo "${GREEN}✅ Docker image built${NC}"

# Run Docker Compose
docker-up:
	@echo "🚀 Starting containers..."
	@$(DOCKER_COMPOSE) up -d
	@echo "${GREEN}✅ Containers started${NC}"

# Stop Docker Compose
docker-down:
	@echo "🛑 Stopping containers..."
	@$(DOCKER_COMPOSE) down
	@echo "${GREEN}✅ Containers stopped${NC}"

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@echo "${GREEN}✅ Temporary files removed${NC}"

# Default target shows help
default: help
