# Data Models

This section describes the main data models used in the API and their relationships.

## Users

### User

The model represents a user of the system.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique user identifier |
| email | string | User email (unique) |
| hashed_password | string | Hashed password |
| first_name | string | User first name |
| last_name | string | User last name |
| phone | string | Phone number (optional) |
| is_active | boolean | Is the user active? |
| is_verified | boolean | Is the user's email verified? |
| role | enum | User role: 'user', 'barista', 'admin' |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

## Products

### Category

The model represents a product category.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique category identifier |
| name | string | Category name (unique) |
| description | string | Category description (optional) |
| image_url | string | Category image URL (optional) |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

### Product

The model represents a product.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique product identifier |
| name | string | Product name |
| description | string | Product description |
| price | float | Product price |
| stock | int | Quantity in stock |
| is_active | boolean | Is the product active? |
| category_id | int | Category identifier (foreign key) |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

## Cart

### Cart

The model represents a user's cart.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique cart identifier |
| user_id | int | User identifier (foreign key) |
| total_amount | float | Total cost of items in the cart |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

### CartItem

The model represents an item in the cart.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique cart item identifier |
| cart_id | int | Cart identifier (foreign key) |
| product_id | int | Product identifier (foreign key) |
| quantity | int | Product quantity |
| price | float | Price per unit of product |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

## Orders

### Order

The model represents an order.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique order identifier |
| user_id | int | User identifier (foreign key) |
| status | enum | Order status: 'pending', 'processing', 'completed', 'cancelled' |
| total_amount | float | Total cost of the order |
| shipping_address | string | Shipping address |
| notes | string | Additional notes (optional) |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

### OrderItem

The model represents an order item.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique order item identifier |
| order_id | int | Order identifier (foreign key) |
| product_id | int | Product identifier (foreign key) |
| quantity | int | Product quantity |
| price | float | Price per unit of product |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

## Chat

### ChatSession

The model represents a chat session.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique session identifier |
| user_id | int | User identifier (foreign key) |
| is_active | boolean | Is the session active? |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

### ChatMessage

The model represents a chat message.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique message identifier |
| session_id | int | Session identifier (foreign key) |
| sender_type | string | Sender type: 'user' or 'system' |
| content | string | Message content |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

## Information

### CoffeeShopLocation

The model represents information about a physical coffee shop location.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique identifier |
| name | string | Coffee shop name |
| address | string | Address |
| city | string | City |
| state | string | State/Region (optional) |
| zip_code | string | Zip code |
| country | string | Country |
| phone | string | Phone (optional) |
| email | string | Email (optional) |
| latitude | float | Geographic latitude (optional) |
| longitude | float | Geographic longitude (optional) |
| is_active | boolean | Is the location active? |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

### StaticInfo

The model represents static information.

| Field | Type | Description |
| ---- | --- | -------- |
| id | int | Unique identifier |
| key | string | Key (unique) |
| value | string | Value |
| created_at | datetime | Date and time of creation |
| updated_at | datetime | Date and time of last update |

## Relationship Diagram

```
User 1---* Order
User 1---1 Cart
Cart 1---* CartItem
CartItem *---1 Product
Order 1---* OrderItem
OrderItem *---1 Product
Product *---1 Category
User 1---* ChatSession
ChatSession 1---* ChatMessage
```
