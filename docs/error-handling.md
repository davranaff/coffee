# Error Handling

This section describes the standard error codes, response formats, and recommendations for error handling in the Coffee Shop API.

## Standard HTTP Status Codes

The API uses standard HTTP status codes to indicate the result of a request:

| Code | Description |
| --- | -------- |
| 200 | OK - Request executed successfully |
| 201 | Created - Resource successfully created |
| 204 | No Content - Request executed successfully, but response does not contain data |
| 400 | Bad Request - Invalid request |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Access denied |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Conflict during request processing |
| 422 | Unprocessable Entity - Invalid data in request |
| 429 | Too Many Requests - Request limit exceeded |
| 500 | Internal Server Error - Internal server error |

## Error Response Format

All errors are returned in a uniform format:

```json
{
  "detail": "Error description"
}
```

For more detailed errors, an extended format may be used:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "password"],
      "msg": "password must be at least 8 characters long",
      "type": "value_error.string_too_short"
    }
  ]
}
```

## API-Specific Errors

### Authentication Errors

| Code | Error | Description |
| --- | ------ | -------- |
| 401 | InvalidCredentialsError | Invalid credentials |
| 401 | ExpiredTokenError | Token has expired |
| 401 | InvalidTokenError | Invalid token |
| 400 | InvalidVerificationCodeError | Invalid verification code |
| 400 | DuplicateEmailError | Email already registered |

### Resource Errors

| Code | Error | Description |
| --- | ------ | -------- |
| 404 | UserNotFoundError | User not found |
| 404 | ProductNotFoundError | Product not found |
| 404 | CategoryNotFoundError | Category not found |
| 404 | CartNotFoundError | Cart not found |
| 404 | OrderNotFoundError | Order not found |

### Business Logic Errors

| Code | Error | Description |
| --- | ------ | -------- |
| 400 | InsufficientStockError | Insufficient stock |
| 400 | EmptyCartError | Cart is empty |
| 400 | InvalidOrderStatusError | Invalid order status |
| 409 | OrderAlreadyCompletedError | Order already completed and cannot be changed |

## Error Handling Recommendations

1. **Validate input data on the client side** before sending a request to reduce the number of 400 errors.

2. **Always check the response status codes** and handle errors appropriately.

3. **Implement retry attempts with exponential backoff** for temporary errors, such as 429 or 500.

4. **Automatically update the access token**, if you receive a 401 ExpiredTokenError, using the refresh token.

5. **Inform users of errors in a user-friendly way**, but do not reveal technical details.

## Error Handling Examples

### JavaScript (fetch)

```javascript
async function fetchData(url, token) {
  try {
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();

      if (response.status === 401) {        // Token update or redirect to login page
        handleAuthError(errorData);
        return;
      }

      throw new Error(errorData.detail || 'Unknown error');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}
```

### Python (requests)

```python
import requests

def fetch_data(url, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for 4XX/5XX responses

        return response.json()
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()

        if e.response.status_code == 401:
            # Token update or redirect to login page
            handle_auth_error(error_data)
            return

        raise Exception(error_data.get("detail", "Unknown error"))
    except requests.exceptions.RequestException as e:
        # Network error or another problem with the request
        raise Exception(f"Network error: {str(e)}")
