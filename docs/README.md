# Coffee Shop API Documentation

Welcome to the Coffee Shop API documentation. This API provides functionality for an online coffee shop, including user management, products, orders, and other features.

## Table of Contents

- [Getting Started](getting-started.md)
- [Authentication](authentication.md)
- [API Endpoints](api-endpoints.md)
- [Data Models](data-models.md)
- [Error Handling](error-handling.md)

## System Overview

The Coffee Shop API system is built on FastAPI and provides a REST API for interacting with the application. The API uses asynchronous requests for optimal performance and supports various features for managing users, products, orders, and other aspects of the online coffee shop.

### Key Features

- **Authentication and Authorization**: Secure registration, login, and user management
- **Product Management**: CRUD operations for products and categories
- **Shopping Cart**: User cart management
- **Orders**: Creating and tracking orders
- **Chat**: Chat capabilities with support

### Technical Stack

- **FastAPI**: High-performance web framework for creating API
- **SQLAlchemy**: ORM for database interaction
- **PostgreSQL**: Primary database
- **Alembic**: Database migration tool
- **JWT**: Token-based authentication
- **Pydantic**: Data validation and serialization

## Installation and Setup

See [Getting Started](getting-started.md) for installation and setup instructions.

## Using the API

See [API Endpoints](api-endpoints.md) for detailed information on available endpoints and usage examples.

## Data Models

See [Data Models](data-models.md) for information on data structures and their relationships.
