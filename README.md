# Coffee Shop API

Backend application for coffee shop management. The API provides functionality for menu management, orders, users, and authentication.

## Technologies

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT authentication
- Docker / Docker Compose

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Docker (optional)

### Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/coffee-shop-api.git
   cd coffee-shop-api
   ```

2. Set up the project:
   ```
   make setup
   ```
   
   This will create an `.env` file from the template, install dependencies, and create databases.

3. Apply migrations:
   ```
   make migrate
   ```

## Running the Application

### Local Run

```
make run
```

The application will be available at http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker

To run with Docker:

```
make docker-up
```

## Development

### Managing Migrations

Creating a new migration:
```
make migrate-create msg="description of changes"
```

Applying migrations:
```
make migrate
```

Rollback migration:
```
make migrate-down
```

Check migration status:
```
make migrate-status
```

### Tests

Run tests:
```
make test
```

Run tests with coverage report:
```
make test-cov
```

## Project Structure

```
├── app/                    # Application source code
│   ├── api/                # API endpoints
│   ├── core/               # Configuration and settings
│   ├── db/                 # Database modules
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── utils/              # Helper functions
├── alembic/                # Alembic migrations
├── tests/                  # Tests
├── Dockerfile              # Docker image build file
├── docker-compose.yml      # Docker Compose configuration
├── Makefile                # Project management commands
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## License

MIT 