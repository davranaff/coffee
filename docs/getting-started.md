# Getting Started

This section describes the steps for setting up and running the Coffee Shop API project.

## Requirements

To work with the project, you need:

- Python 3.9 or higher
- PostgreSQL 13 or higher
- Docker and Docker Compose (optional)
- Make (optional, for using Makefile)

## Quick Setup with Makefile

The project uses Makefile to automate tasks. To see a list of all available commands:

```bash
make help
```

### Full Project Setup

```bash
# Complete setup (creating .env, databases, migrations)
make setup
```

### Running the Server

```bash
# Run development server
make run

# Run in production mode
make run-prod
```

### Working with the Database

```bash
# Create databases
make db

# Apply migrations
make migrate

# Create a new migration
make migration m="Migration description"

# Rollback migration
make downgrade

# Check migration status
make migrate-status
```

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage report
make test-cov
```

### Working with Docker

```bash
# Build image
make docker-build

# Start containers
make docker-up

# Stop containers
make docker-down
```

## Quick Setup with Script

Alternatively, you can use the `setup_project.py` script for quick project setup:

```bash
# Make script executable
chmod +x setup_project.py

# Run complete project setup (create .env, databases, apply migrations)
./setup_project.py --all

# Or perform individual steps:
./setup_project.py --env     # Create .env file
./setup_project.py --db      # Create databases
./setup_project.py --scripts # Make scripts executable
./setup_project.py --migrate # Apply migrations
```

## Manual Installation

If you prefer manual setup, follow the instructions below.

### Clone the Repository

```bash
git clone https://github.com/username/coffee-shop-api.git
cd coffee-shop-api
```

### Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
# or
venv\Scripts\activate     # for Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

2. Edit the `.env` file, specifying the required parameters:

```
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost/coffee
ASYNC_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost/coffee

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=your-smtp-password
```

## Setting Up the Database

### Using a Local Database

Create a database in PostgreSQL:

```bash
createdb coffee
```

### Using Docker

```bash
docker-compose up -d db
```

## Database Migrations

Before running the application for the first time, you need to apply migrations to create the database schema:

```bash
# Make the migrations script executable
chmod +x migrate.py

# Apply migrations
./migrate.py upgrade head
```

Detailed information about working with migrations can be found in the `migrations/README.md` file.

## Running the Development Server

### Direct Start

```bash
uvicorn app.main:app --reload
```

### Start with Docker

```bash
docker-compose up -d
```

The server will be available at: http://localhost:8000

## API Documentation

After starting the server, Swagger UI documentation is available at:

http://localhost:8000/docs

ReDoc documentation is available at:

http://localhost:8000/redoc

## Testing

To run tests, use the special script:

```bash
# Make the script executable
chmod +x run_tests.py

# Create test database
./run_tests.py --db-init

# Run all tests
./run_tests.py

# Run tests with code coverage
./run_tests.py --cov
```

Detailed information about testing can be found in the `tests/README.md` file.

## Project Structure

Main directories and files of the project:

- `app/` - main application code
  - `api/` - API handlers
  - `core/` - basic settings and utilities
  - `crud/` - database operations
  - `db/` - database models and connection
  - `schemas/` - data schemas (Pydantic models)
  - `services/` - application business logic
  - `main.py` - application entry point
- `migrations/` - Alembic migration files
- `tests/` - automated tests
- `docs/` - project documentation
- `.env.example` - example environment variables file
- `docker-compose.yml` - Docker Compose configuration
- `Dockerfile` - Docker configuration
- `requirements.txt` - Python dependencies
- `migrate.py` - script for managing migrations
- `run_tests.py` - script for running tests
- `setup_project.py` - script for automatic project setup
- `Makefile` - file with commands for task automation
