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

@pytest.fixture(scope="session")
def client():
    """Return a TestClient bound to the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def auth_header():
    """Placeholder header for routes requiring Authorization."""
    return {"Authorization": "Bearer test-token"}


@pytest.fixture
def meal_payload():
    return {
        "title": "Free pizza slices",
        "description": "Leftover cheese & veggie slices in Dorm A lounge",
        "location": "Dorm A, 2nd floor lounge",
        "allergens": ["gluten", "dairy"],
        "expires_at": "2099-12-31T23:59:59Z",
        "quantity": 6,
        "is_vegan": False,
        "is_vegetarian": True
    }


@pytest.fixture
def update_meal_payload():
    return {
        "description": "About 3 slices left, please bring your own plate.",
        "quantity": 3
    }


@pytest.fixture
def profile_update_payload():
    return {"full_name": "Test Student", "bio": "Likes sharing leftovers."}


@pytest.fixture
def dietary_prefs_payload():
    return {
        "vegetarian": True,
        "vegan": False,
        "gluten_free": False,
        "nut_allergy": False
    }


@pytest.fixture
def social_links_payload():
    return {"instagram": "test.student", "telegram": None, "phone": None}