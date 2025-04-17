from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User


class TestAuthAPI:
    """Test cases for authentication API endpoints"""

    def test_login(self, client: TestClient, test_user: User):
        """Test login endpoint"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user.email, "password": "password123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials"""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "wrong@example.com", "password": "wrongpassword"}
        )

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_register(self, client: TestClient):
        """Test register endpoint"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "new_register@example.com",
                "password": "Password123",
                "first_name": "New",
                "last_name": "Register"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new_register@example.com"
        assert data["first_name"] == "New"
        assert data["last_name"] == "Register"
        assert data["is_active"] is True
        assert data["is_verified"] is False
        assert data["role"] == "user"
        assert "id" in data

    def test_register_duplicate_email(self, client: TestClient, test_user: User):
        """Test register with duplicate email"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user.email,
                "password": "Password123",
                "first_name": "Duplicate",
                "last_name": "Email"
            }
        )

        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_verify(self, client: TestClient, db_session: AsyncSession):
        """Test user verification endpoint"""
        # First register a user
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "to_verify@example.com",
                "password": "Password123",
                "first_name": "To",
                "last_name": "Verify"
            }
        )

        assert register_response.status_code == 201

        # For testing, set verification code directly in database
        verification_code = "123456"
        user = db_session.query(User).filter(User.email == "to_verify@example.com").first()
        user.verification_code = verification_code
        db_session.commit()

        # Now verify the user
        verify_response = client.post(
            "/api/v1/auth/verify",
            json={
                "email": "to_verify@example.com",
                "verification_code": verification_code
            }
        )

        assert verify_response.status_code == 200
        data = verify_response.json()
        assert data["is_verified"] is True

    def test_verify_invalid_code(self, client: TestClient, db_session: AsyncSession):
        """Test verification with invalid code"""
        # First register a user
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid_verify@example.com",
                "password": "Password123",
                "first_name": "Invalid",
                "last_name": "Verify"
            }
        )

        assert register_response.status_code == 201

        # Set verification code in database
        verification_code = "123456"
        user = db_session.query(User).filter(User.email == "invalid_verify@example.com").first()
        user.verification_code = verification_code
        db_session.commit()

        # Try to verify with wrong code
        verify_response = client.post(
            "/api/v1/auth/verify",
            json={
                "email": "invalid_verify@example.com",
                "verification_code": "wrong_code"
            }
        )

        assert verify_response.status_code == 400
        data = verify_response.json()
        assert "detail" in data

    def test_refresh_token(self, client: TestClient, test_user: User):
        """Test token refresh endpoint"""
        # First login to get tokens
        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user.email, "password": "password123"}
        )

        assert login_response.status_code == 200
        login_data = login_response.json()
        refresh_token = login_data["refresh_token"]

        # Now refresh the token
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert refresh_response.status_code == 200
        refresh_data = refresh_response.json()
        assert "access_token" in refresh_data
        assert "refresh_token" in refresh_data
        assert refresh_data["token_type"] == "bearer"

    def test_me(self, client: TestClient, test_user: User, user_token: str):
        """Test me endpoint"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email
        assert data["first_name"] == test_user.first_name
        assert data["last_name"] == test_user.last_name

    def test_me_no_token(self, client: TestClient):
        """Test me endpoint without token"""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
