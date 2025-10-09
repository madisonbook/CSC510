import pytest
from fastapi.testclient import TestClient
from app.main import app
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import get_database

# Setup a test MongoDB database
TEST_MONGO_URL = "mongodb://localhost:27017"
TEST_DB_NAME = "test_db"

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    client = AsyncIOMotorClient(TEST_MONGO_URL)
    db = client[TEST_DB_NAME]

    # Patch your app’s get_database dependency
    app.dependency_overrides[get_database] = lambda: db

    yield db

    # Clean up after tests
    await client.drop_database(TEST_DB_NAME)
    client.close()