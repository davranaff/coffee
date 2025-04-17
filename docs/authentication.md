# Authentication

The Coffee Shop API authentication system is based on JWT (JSON Web Token) and provides a secure way to authenticate users.

## User Registration

To register a new user, send a POST request to `/api/v1/auth/register` with the user's data:

```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

After successful registration, the user will receive an email with a verification code.

## User Verification

After registration, the user must confirm their email by sending a POST request to `/api/v1/auth/verify` with the verification code:

```json
{
  "email": "user@example.com",
  "verification_code": "123456"
}
```

## Login

To log in, send a POST request to `/api/v1/auth/login` with the form data:

```
username=user@example.com&password=securePassword123
```

In response, you will receive:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Using the Access Token

To access protected API resources, add the access token to the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Token Refresh

When the access token expires, you can get a new one by sending a POST request to `/api/v1/auth/refresh` with the refresh token:

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Getting Current User Information

To get information about the current authenticated user, send a GET request to `/api/v1/auth/me` with the access token in the `Authorization` header.

## User Roles

The following user roles are defined in the system:

- **user**: Ordinary user with basic rights
- **barista**: Coffee shop worker with additional rights for processing orders
- **admin**: Administrator with full access to the system

## JWT Token Structure

The access token contains the following information:

- **sub**: User ID
- **exp**: Token expiration time
- **type**: Token type ("access" or "refresh")

## Security

- Passwords are stored encrypted (using bcrypt)
- Tokens have a limited lifetime
- Refresh tokens can be revoked
- All authentication requests are protected against brute-force attacks
