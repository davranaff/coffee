# Testing

This section describes how to run and write tests for the Coffee Shop API project.

## Running Tests

For convenience, use the `run_tests.py` script in the project root directory to run tests:

```bash
# Make the script executable (run once)
chmod +x run_tests.py

# Run all tests
./run_tests.py

# Create a test database and run tests
./run_tests.py --db-init

# Run tests with code coverage
./run_tests.py --cov

# Run tests with detailed output
./run_tests.py -v

# Run tests for a specific module
./run_tests.py tests/test_auth_service.py

# Run tests containing a specific word in the name
./run_tests.py -k "auth"

# Run tests by marker
./run_tests.py -m "asyncio"

# Coverage report in HTML format
./run_tests.py --cov --cov-report=html
```

To run tests without using the script, you can directly use pytest:

```bash
# Run all tests
pytest

# Run tests with code coverage
pytest --cov=app
```

## Test Structure

Tests are organized as follows:

- `conftest.py` - configuration for tests and common fixtures
- `test_*.py` - files with tests

## Fixtures

The project provides the following fixtures for tests:

- `event_loop` - event loop for asynchronous tests
- `test_db` - test database
- `db_session` - database session
- `client` - test client for FastAPI
- `test_user` - test user with the role "user"
- `test_admin` - test user with the role "admin"
- `user_token` - JWT token for the test user
- `admin_token` - JWT token for the test administrator

### Example of using fixtures

```python
@pytest.mark.asyncio
async def test_create_order(db_session, test_user):
    # Test using the database session and test user
    pass

def test_get_order_api(client, user_token):
    # Test API using the test client and token
    pass
```

## Adding Tests

When adding new tests, follow these recommendations:

1. Create a new file `test_<module_name>.py` for each module
2. Organize tests into classes for each component
3. Use the `@pytest.mark.asyncio` marker for asynchronous tests
4. Use fixtures to set up the test environment
5. Check code coverage using the `--cov` option

### Example Test Class

```python
import pytest
from app.your_module import YourClass

class TestYourClass:
    """Tests for YourClass"""

    @pytest.mark.asyncio
    async def test_async_method(self, db_session):
        """Test async method"""
        obj = YourClass(db_session)
        result = await obj.some_method()
        assert result == expected_value

    def test_sync_method(self):
        """Test sync method"""
        obj = YourClass()
        result = obj.some_sync_method()
        assert result == expected_value
```
