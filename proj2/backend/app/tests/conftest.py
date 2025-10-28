"""
Pytest configuration and shared fixtures for meal API tests.
Place this file in your tests/ directory as: app/tests/conftest.py
"""
import pytest
import pytest_asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Test MongoDB configuration
TEST_MONGO_URL = os.environ.get("TEST_MONGO_URL", "mongodb://localhost:27018")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME", "test_meal_db")

# Force debug output to stderr so it's visible
import sys
print(f"\n{'='*60}", file=sys.stderr, flush=True)
print(f"[TEST CONFIG] Using MongoDB URL: {TEST_MONGO_URL}", file=sys.stderr, flush=True)
print(f"[TEST CONFIG] Database: {TEST_DB_NAME}", file=sys.stderr, flush=True)
print(f"{'='*60}\n", file=sys.stderr, flush=True)

# Use function scope for mongo_client to avoid event loop issues
@pytest_asyncio.fixture(scope="function")
async def mongo_client():
    """
    Create a MongoDB client for each test function.
    This ensures each test uses the correct event loop.
    """
    client = AsyncIOMotorClient(TEST_MONGO_URL, serverSelectionTimeoutMS=5000)
    
    # Verify connection
    try:
        await client.admin.command('ping')
    except Exception as e:
        pytest.fail(f"Failed to connect to test MongoDB at {TEST_MONGO_URL}: {e}")
    
    yield client
    
    # Cleanup
    client.close()

def pytest_configure(config):
    """
    Pytest hook for initial configuration.
    """
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )