# API Endpoints

Below are the main API endpoints with a description of their functionality. All URLs start with the base path `/api/v1`.

## Authentication

| Method | Path | Description |
| ----- | ---- | -------- |
| POST | `/auth/register` | Registration of a new user |
| POST | `/auth/login` | Login and token acquisition |
| POST | `/auth/verify` | User email verification |
| POST | `/auth/refresh` | Access token refresh |
| GET | `/auth/me` | Get information about the current user |

## Users

| Method | Path | Description |
| ----- | ---- | -------- |
| GET | `/users/` | Get list of users (only for administrators) |
| GET | `/users/{user_id}` | Get information about a specific user |
| PATCH | `/users/{user_id}` | Update user information |
| DELETE | `/users/{user_id}` | Delete a user |

## Products

| Method | Path | Description |
| ----- | ---- | -------- |
| GET | `/products/` | Get list of products |
| GET | `/products/{product_id}` | Get information about a specific product |
| POST | `/products/` | Create a new product (only for administrators) |
| PATCH | `/products/{product_id}` | Update product information (only for administrators) |
| DELETE | `/products/{product_id}` | Delete a product (only for administrators) |

## Categories

| Method | Path | Description |
| ----- | ---- | -------- |
| GET | `/categories/` | Get list of categories |
| GET | `/categories/{category_id}` | Get information about a specific category |
| GET | `/categories/{category_id}/products` | Get products in a category |
| POST | `/categories/` | Create a new category (only for administrators) |
| PATCH | `/categories/{category_id}` | Update category information (only for administrators) |
| DELETE | `/categories/{category_id}` | Delete a category (only for administrators) |

## Cart

| Method | Path | Description |
| ----- | ---- | -------- |
| GET | `/cart/` | Get the contents of the current user's cart |
| POST | `/cart/items/` | Add a product to the cart |
| PATCH | `/cart/items/{item_id}` | Update the quantity of a product in the cart |
| DELETE | `/cart/items/{item_id}` | Remove a product from the cart |
| DELETE | `/cart/clear` | Clear the cart |

## Orders

| Method | Path | Description |
| ----- | ---- | -------- |
| GET | `/orders/` | Get list of orders for the current user |
| GET | `/orders/{order_id}` | Get information about a specific order |
| POST | `/orders/` | Create a new order |
| PATCH | `/orders/{order_id}` | Update order status |
| DELETE | `/orders/{order_id}` | Cancel an order |

## Chat

| Method | Path | Description |
| ----- | ---- | -------- |
| GET | `/chat/sessions/` | Get list of chat sessions for the current user |
| GET | `/chat/sessions/{session_id}` | Get messages from a specific chat session |
| POST | `/chat/sessions/` | Create a new chat session |
| POST | `/chat/sessions/{session_id}/messages` | Send a message to the chat |
| DELETE | `/chat/sessions/{session_id}` | Close a chat session |

## Information

| Method | Path | Description |
| ----- | ---- | -------- |
| GET | `/info/locations/` | Get list of coffee shops |
| GET | `/info/locations/{location_id}` | Get information about a specific coffee shop |
| GET | `/info/company` | Get information about the company |
| GET | `/info/static/{key}` | Get static information by key |

## Pagination and Sorting

Many requests return lists of objects and support pagination and sorting parameters:

- `limit`: Limit the number of results (default 10, maximum 100)
- `offset`: Offset for pagination
- `sort`: Field for sorting
- `order`: Sorting order (`asc` or `desc`)

Example:

```
GET /api/v1/products?limit=20&offset=40&sort=price&order=desc
```

## Filtering

Many endpoints support filtering by various fields. For example:

```
GET /api/v1/products?category_id=5&price_min=10&price_max=50&is_active=true
```

## Response Format

All responses are returned in JSON format.

Standard response format for lists:

```json
{
  "items": [...],
  "total": 100,
  "limit": 10,
  "offset": 0
}
```

Standard response format for errors:

```json
{
  "detail": "Error description"
}
```
