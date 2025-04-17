import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.product import Product, Category
from app.db.models.order import Order, OrderItem


@pytest.fixture
async def test_category(db_session: AsyncSession):
    """Create a test category"""
    category = Category(
        name="Test Category",
        description="Test category description"
    )
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)
    return category


@pytest.fixture
async def test_product(db_session: AsyncSession, test_category):
    """Create a test product"""
    product = Product(
        name="Test Product",
        description="Test product description",
        price=9.99,
        stock=100,
        category_id=test_category.id
    )
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    return product


@pytest.fixture
async def test_order(db_session: AsyncSession, test_user, test_product):
    """Create a test order"""
    order = Order(
        user_id=test_user.id,
        status="pending",
        total_amount=9.99,
        shipping_address="123 Test St, Test City, 12345"
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)

    # Add an order item
    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=1,
        price=9.99
    )
    db_session.add(order_item)
    await db_session.commit()

    return order


class TestOrderAPI:
    """Test cases for order API endpoints"""

    def test_create_order(self, client: TestClient, user_token: str, test_product: Product):
        """Test create order endpoint"""
        response = client.post(
            "/api/v1/orders/",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "status": "pending",
                "total_amount": 9.99,
                "shipping_address": "123 Test St, Test City, 12345",
                "items": [
                    {
                        "product_id": test_product.id,
                        "quantity": 1
                    }
                ]
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "pending"
        assert data["total_amount"] == 9.99
        assert data["shipping_address"] == "123 Test St, Test City, 12345"
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == test_product.id
        assert data["items"][0]["quantity"] == 1

    def test_get_orders(self, client: TestClient, user_token: str, test_order: Order):
        """Test get orders endpoint"""
        response = client.get(
            "/api/v1/orders/",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Verify first order in list
        order = next((o for o in data if o["id"] == test_order.id), None)
        assert order is not None
        assert order["status"] == test_order.status
        assert order["total_amount"] == test_order.total_amount
        assert order["shipping_address"] == test_order.shipping_address

    def test_get_order(self, client: TestClient, user_token: str, test_order: Order):
        """Test get order by ID endpoint"""
        response = client.get(
            f"/api/v1/orders/{test_order.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_order.id
        assert data["status"] == test_order.status
        assert data["total_amount"] == test_order.total_amount
        assert data["shipping_address"] == test_order.shipping_address
        assert len(data["items"]) == 1

    def test_update_order(self, client: TestClient, user_token: str, test_order: Order):
        """Test update order endpoint"""
        response = client.patch(
            f"/api/v1/orders/{test_order.id}",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "status": "processing",
                "shipping_address": "456 Update St, Update City, 67890"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_order.id
        assert data["status"] == "processing"  # Updated status
        assert data["shipping_address"] == "456 Update St, Update City, 67890"  # Updated address

    def test_delete_order(self, client: TestClient, user_token: str, test_order: Order):
        """Test delete order endpoint"""
        response = client.delete(
            f"/api/v1/orders/{test_order.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == 204

        # Verify order is deleted
        get_response = client.get(
            f"/api/v1/orders/{test_order.id}",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        assert get_response.status_code == 404

    def test_unauthorized_access(self, client: TestClient):
        """Test unauthorized access to orders"""
        response = client.get("/api/v1/orders/")

        assert response.status_code == 401

        response = client.post("/api/v1/orders/")

        assert response.status_code == 401
